from webapp.db import db, Model

class Person(db.EmbeddedDocument):
    name = db.StringField()
    email = db.EmailField()


class Enclosure(db.EmbeddedDocument):
    url = db.URLField()
    length = db.IntField()
    type = db.StringField()


class Episode(db.EmbeddedDocument):
    title = db.StringField(required=True)
    subtitle = db.StringField()
    description = db.StringField()
    author = db.StringField()
    guid = db.StringField(required=True)
    published = db.DateTimeField(required=True)
    image = db.URLField()
    duration = db.IntField()
    explicit = db.IntField()
    enclosure = db.EmbeddedDocumentField(Enclosure, required=True)



class Podcast(Model):
    url = db.URLField(required=True, unique=True)
    title = db.StringField(required=True)
    author = db.StringField(required=True)
    description = db.StringField()
    language = db.StringField()
    copyright = db.StringField()
    image = db.StringField()
    categories = db.ListField(db.StringField())
    owner = db.EmbeddedDocumentField(Person)
    last_fetched = db.DateTimeField()
    previous_urls = db.ListField(db.URLField(), default=[])
    complete = db.BooleanField()
    episodes = db.EmbeddedDocumentListField(Episode)
    subscribers = db.IntField(default=0)

    @classmethod
    def get_by_url(cls, url):
        return cls.objects(db.Q(url=url) or db.Q(previous_urls=url)).first()

    @classmethod
    def get_multi_by_url(cls, urls):
        """Given a list of urls, returns a dictionary mapping from url to podcast."""
        podcasts = cls.objects(db.Q(url__in=urls) or db.Q(previous_urls__in=urls))
        return {podcast.url : podcast for podcast in podcasts}