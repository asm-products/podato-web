from flask.ext.mongoalchemy import MongoAlchemy

db = MongoAlchemy()

def init_db(app):
    db.init_app(app)


class Model(db.Document):
    def put(self, *args, **kwargs):
        self.save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.remove(*args, **kwargs)

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)


class IDMixin(object):
    """DEPRECATED This class is no longer necessary."""""
    pass
