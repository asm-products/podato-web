from google.appengine.ext import ndb

from model_utils import IDMixin
from podcasts import crawler


class Person(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()


class Enclosure(ndb.Model):
    url = ndb.StringProperty(indexed=False)
    length = ndb.IntegerProperty(indexed=False)
    type = ndb.StringProperty(indexed=False)


class Episode(ndb.Model):
    title = ndb.StringProperty(indexed=False)
    subtitle = ndb.StringProperty(indexed=False)
    description = ndb.TextProperty()
    author = ndb.StringProperty(indexed=False)
    guid = ndb.StringProperty()
    published = ndb.DateTimeProperty()
    image = ndb.StringProperty(indexed=False)
    duration = ndb.IntegerProperty(indexed=False)
    explicit = ndb.IntegerProperty()
    enclosure = ndb.StructuredProperty(Enclosure)


class Podcast(ndb.Model, IDMixin):
    title = ndb.StringProperty(indexed=False)
    author = ndb.StringProperty()
    description = ndb.TextProperty()
    language = ndb.StringProperty()
    copyright = ndb.StringProperty(indexed=False)
    image = ndb.StringProperty(indexed=False)
    categories = ndb.StringProperty(repeated=True)
    owner = ndb.StructuredProperty(Person, indexed=False)
    last_fetched = ndb.DateTimeProperty()
    moved_to = ndb.StringProperty(indexed=False)
    complete = ndb.BooleanProperty()
    episodes = ndb.StructuredProperty(Episode, repeated=True)


class SubscriptionHolder(object):
    subscriptions = ndb.KeyProperty(Podcast, repeated=True)

    def subscribe(self, key):
        if isinstance(key, Podcast):
            key = key.key
        if key in self.subscriptions:
            return False
        self.subscriptions.append(key)
        return True

    def subscribe_by_url(self, url):
        podcast = Podcast.get_by_id(url, use_cache=False, use_memcache=False)
        if podcast == None:
            crawler.fetch(url)
            return self.subscribe_by_url(url)
        return self.subscribe(podcast.key)

    def unsubscribe(self, key):
        if isinstance(key, Podcast):
            key = key.key

        try:
            self.subscriptions.remove(key)
            return True
        except ValueError:
            return False

    def get_subscriptions(self):
        return ndb.get_multi(self.subscriptions)