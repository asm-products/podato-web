from flask.ext.mongoengine import MongoEngine


db = MongoEngine()

def init_db(app):
    db.init_app(app)


class Model(db.Document):
    meta = {'abstract': True}

    def put(self, *args, **kwargs):
        self.save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.remove(*args, **kwargs)

    @classmethod
    def get_by_id(cls, id):
        return cls.objects.with_id(id)






































    @property
    def query(self):
        """The 'objects' property has the same function the 'query property has
           in App Engine's ndb module, so this makes porting easier."""
        return self.objects


class IDMixin(object):
    """DEPRECATED This class is no longer necessary."""""
    pass
