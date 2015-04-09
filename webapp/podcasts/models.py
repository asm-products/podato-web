from google.appengine.ext import ndb

from model_utils import IDMixin


class Person(ndb.Model):
    name = ndb.StringProperty()
    email = ndb.StringProperty()


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


class Podcast(ndb.Model, IDMixin)
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

    def subscribe(self, podcast):
        if podcast.key in self.subscriptions:
            return False
        self.subscriptions.append(podcast.key)
        return True

    def unsubscribe(self, podcast):
        try:
            self.subscriptions.remove(podcast.key)
            return True
        except ValueError:
            return False

    def get_subscriptions(self):
        return ndb.get_multi(self.subscriptions)