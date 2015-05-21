from db import db, Model
from model_utils import IDMixin
from podcasts import crawler


class Person(db.EmbeddedDocument):
    name = db.StringField()
    email = db.EmailField()


class Enclosure(db.EmbeddedDocument):
    url = db.URLField()
    length = db.IntegerField()
    type = db.StringField()


class Episode(db.EmbeddedDocument):
    title = db.StringField(required=True)
    subtitle = db.StringField()
    description = db.StringField()
    author = db.StringField()
    guid = db.StringField(required=True)
    published = db.DateTimeField(required=True)
    image = db.URLField()
    duration = db.IntegerField()
    explicit = db.IntegerField()
    enclosure = db.EmbeddedDocumentField(Enclosure, required=True)


class Podcast(Model):
    url = db.URLField(primary_key=True)
    title = db.StringField(required=True)
    author = db.StringField(required=True)
    description = db.StringField()
    language = db.StringField()
    copyright = db.StringField()
    image = db.StringField()
    categories = db.ListField(db.StringField)
    owner = db.EmbeddedDocumentField(Person)
    last_fetched = db.DateTimeField()
    moved_to = db.URLField()
    complete = db.BooleanField()
    episodes = db.ListField(db.EmbeddedField(Episode))

    @classmethod
    def get_by_url(cls, url, **kwargs):
        podcast = cls.get_by_id(url, **kwargs)
        if podcast and podcast.moved_to:
            return cls.get_by_url(url, **kwargs)
        return podcast


class SubscriptionHolder(object):
    subscriptions = db.ListField(db.ReferenceField(Podcast, reverse_delete_rule=db.PULL))

    def subscribe(self, podcast):
        if podcast in self.subscriptions:
            return False
        self.modify(push__subscriptions=podcast)
        return True

    def subscribe_by_url(self, url):
        podcast = Podcast.get_by_url(url, use_cache=False, use_memcache=False)
        if podcast == None:
            crawler.fetch(url)
            return self.subscribe_by_url(url)
        return self.subscribe(podcast)

    def unsubscribe(self, podcast):
        return self.modify(pull_subscriptions=podcast)

    def unsubscribe_by_url(self, url):
        podcast = Podcast.get_by_url
        return self.unsubscribe(podcast)
