import datetime
import time

import feedparser

from webapp import utils
from webapp.podcasts.models import  Podcast, Episode, Person, Enclosure

PODATO_USER_AGENT = "Podato Crawler"

class FetchError(Exception):
    pass

def fetch(url):
    """This fetches a podcast and stores it in the db. It assumes that it only gets called
    by Podcast.get_by_url, or some other method that knows whether a given podcast has
    already been fetched."""
    return Podcast(**_fetch_podcast_data(url)).put()

def _fetch_podcast_data(url):
    utils.validate_url(url, allow_hash=False)
    parsed = feedparser.parse(url, agent=PODATO_USER_AGENT)
    return _handle_feed(url, parsed)

def _handle_feed(url, parsed):
    moved_to = None
    if parsed.status == 404:
        raise FetchError("Podcast not found: %s" % (url))
    if parsed.status == 401:
        raise FetchError("This podcast feed requires authentication.")
    elif parsed.status == 410:
        raise FetchError("Podcast no longer available: %s" % (url))
    elif parsed.status == 301: # Permanent redirect
        moved_to = parsed.href
    elif parsed.status == 304: # Not modified
        return {}
    elif parsed.status not in [200, 302, 303, 307]:
        raise FetchError("Got an unexpected response from podcast server: %v" % parsed.status)

    return {
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
        "episodes": [_make_episode(entry) for entry in parsed.entries],
        "moved_to": moved_to
    }


def _make_episode(entry):
    return Episode(
        title=entry.title,
        subtitle=entry.subtitle,
        description=entry.get("content", [{}, {}])[1].get("value") or entry.description,
        author=entry.author,
        guid=entry.guid,
        published=datetime.datetime.fromtimestamp(
            time.mktime(entry.published_parsed
        )),
        image=entry.get("image", {}).get("href"),  #The use of .get ensures no errors are raised when there's no episode image.
        duration=_parse_duration(entry),
        explicit=_parse_explicit(entry),
        enclosure=Enclosure(type=entry.enclosures[0].get("type"),
                              url=entry.enclosures[0].href,
                              length=int(entry.enclosures[0].length)
        )
    )

def _parse_duration(entry):
    parts = entry.itunes_duration.split(":")
    d = 0
    for i in xrange(min(len(parts), 3)):
        d += int(parts[-(i+1)]) * 60**i
    return d

def _parse_explicit(entry):
    exp = entry.get("itunes_explicit")
    if exp == "yes":
        return 1
    elif exp == "clean":
        return 2
    else:
        return 0