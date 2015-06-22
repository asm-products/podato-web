import datetime
import time
import logging

import feedparser
from eventlet.green import urllib2

from webapp import utils
from webapp.podcasts.models import  Podcast, Episode, Person, Enclosure
from webapp.async import app, chord

from mongoengine.base import fields

PODATO_USER_AGENT = "Podato Crawler"

class FetchError(Exception):
    pass

class SmartRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        result = urllib2.HTTPRedirectHandler.http_error_302(self, req, fp,
                                                                 code, msg,
                                                                 headers)
        result.status = code
        result.headers = headers
        return result

    http_error_301 = http_error_303 = http_error_307 = http_error_302

@app.task
def fetch(url_or_urls, subscribe=None):
    """This fetches a (list of) podcast(s) and stores it in the db. It assumes that it only gets called
    by Podcast.get_by_url, or some other method that knows whether a given podcast has
    already been fetched.

    If *subscribe* is given, it should be a User instance to be subscribed to the given podcasts."""
    if isinstance(url_or_urls, basestring):
        url_or_urls = [url_or_urls]
    body = _store_podcasts.s()
    if subscribe:
        body.link(_subscribe_user.s(user=subscribe))
    return chord([_fetch_podcast_data.s(url) for url in url_or_urls])(body)


@app.task
def _fetch_podcast_data(url):
    utils.validate_url(url, allow_hash=False)
    try:
        request = urllib2.Request(url)
        opener = urllib2.build_opener(SmartRedirectHandler)
        request.add_header('User-Agent', PODATO_USER_AGENT)
        logging.info("fetching %s" % url)
        resp = opener.open(request)
        parsed = feedparser.parse(resp)
    except urllib2.HTTPError as e:
        raise FetchError(str(e))
    return _handle_feed(url, parsed, getattr(resp, "status", resp.getcode()))

def _handle_feed(url, parsed, code):
    """Handles the parsed result of a feed, putting it into a dict for storage."""
    previous_url = None
    logging.info("response_code: %s" % code)
    if code == 404:
        raise FetchError("Podcast not found: %s" % (url))
    if code == 401:
        raise FetchError("This podcast feed requires authentication.")
    elif code == 410:
        raise FetchError("Podcast no longer available: %s" % (url))
    elif code == 301: # Permanent redirect
        previous_url = url
    elif code == 304: # Not modified
        return {}
    elif code not in [200, 302, 303, 307]:
        raise FetchError("Got an unexpected response from podcast server: %v" % parsed.status)

    try:
        errors = []
        episodes = []
        for entry in parsed.entries:
            episode, ep_errors = _make_episode(entry    )
            if ep_errors:
                errors += ep_errors
            if episode:
                episodes.append(episode)

        d = {
            "url": parsed.href,
            "title": parsed.feed.title,
            "author": parsed.feed.author,
            "description": parsed.feed.description,
            "language": parsed.feed.language,
            "copyright": parsed.feed.get("rights"),
            "image": parsed.feed.image.href,
            "categories": [tag["term"] for tag in parsed.feed.tags],
            "owner": Person(name=parsed.feed.publisher_detail.name,
                            email=parsed.feed.publisher_detail.email),
            "last_fetched": datetime.datetime.now(),
            "complete": parsed.feed.get("itunes_complete") or False,
            "episodes": episodes,
            "errors": errors
        }
        if previous_url:
            d["previous_urls"] = [previous_url]
        return d
    except Exception as e:
        logging.exception("Encountered an exception while parsing %s" % (parsed.href))
        raise


def _make_episode(entry):
    """Crate an Episode object from the given feedparser item."""
    errors = []
    if not entry.get('enclosures'):
         return None, ["Episode %s has no enclosure."]
    try:
        episode = Episode(
            title=entry.title,
            subtitle=entry.subtitle,
            description=_get_episode_description(entry),
            author=entry.author,
            guid=entry.guid,
            published=datetime.datetime.fromtimestamp(
                time.mktime(entry.published_parsed
            )),
            image=entry.get("image", {}).get("href"),  #The use of .get ensures no errors are raised when there's no episode image.
            duration=_parse_duration(entry, errors),
            explicit=_parse_explicit(entry),
            enclosure=Enclosure(type=entry.enclosures[0].get("type"),
                              url=entry.enclosures[0].href,
                              length=int(entry.enclosures[0].length)
            )
        )
        if episode.image is None:
            errors.append("No image for episode %s" % (episode.guid))
        return episode, errors
    except Exception as e:
        logging.exception("Got an exception while parsing episode: %s." % entry.id)
        return None, [str(e) + " episode: %s" % entry.id]


def _get_episode_description(entry):
    """Pull an episode's description (show notes) from the episode."""
    for content in entry.get('content', []):
        if "html" in content.type:
            return content.value

    return max(entry.get("description", ""), entry.get("summary", ""), key=len)


def _parse_duration(entry, errors):
    """Parse an episode's duration into an integer representing the number of seconds."""
    try:
        parts = entry.itunes_duration.split(":")
        d = 0
        for i in xrange(min(len(parts), 3)):
            d += int(parts[-(i+1)]) * 60**i
    except ValueError:
        logging.exception("Encountered an error while parsing duration %s, %s" % (entry.itunes_duration, entry.id))
        errors.append("Could not parse episode duration: \"%s\", for episode %s." % (entry.itunes_duration, entry.id))
        return 0
    except AttributeError:
        logging.exception("Encountered an error while parsing duration %s" % entry.id)
        errors.append("Episode doesn't have an itunes:duration: %s" % entry.id)
        return 0
    return d

def _parse_explicit(entry):
    """Parse the itunes:explicit tag of an episode."""
    exp = entry.get("itunes_explicit")
    if exp == "yes":
        return 1
    elif exp == "clean":
        return 2
    else:
        return 0

@app.task
def _store_podcasts(podcasts_data):
    """Given a list of dictionaries representing podcasts, store them all in the database."""
    podcasts = [Podcast(**pdata) for pdata in podcasts_data]
    return Podcast.objects.insert(podcasts)

@app.task
def _subscribe_user(podcasts, user):
    """Subscribe the given users to all the podcasts in the list."""
    return user.subscribe_multi(podcasts)