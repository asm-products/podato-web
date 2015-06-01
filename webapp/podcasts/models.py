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
    url = db.StringField(required=True, unique=True)
    title = db.StringField(required=True)
    author = db.StringField(required=True)
    description = db.StringField()
    language = db.StringField()
    copyright = db.StringField()
    image = db.StringField()
    categories = db.ListField(db.StringField())
    owner = db.EmbeddedDocumentField(Person)
    last_fetched = db.DateTimeField()
    moved_to = db.URLField()
    complete = db.BooleanField()
    episodes = db.EmbeddedDocumentListField(Episode)

    @classmethod
    def get_by_url(cls, url):
        podcast = cls.objects(url=url).first()
        if podcast and podcast.moved_to:
            return cls.get_by_url(url, **kwargs)
        return podcast