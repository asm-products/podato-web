import md5

from db import db, Model

from users import auth
from podcasts import SubscriptionHolder
from model_utils import IDMixin
import utils

class User(Model, auth.ProviderTokenHolder, SubscriptionHolder):
    username = db.StringField(required=True)
    primary_email = db.EmailField(required=True)
    email_addresses = db.ListField(db.EmailField())
    avatar_url = db.URLField()

    @classmethod
    def create(cls, username, email, avatar_url=None):
        email_hash = md5.md5(email).hexdigest()
        instance = cls(
            username=utils.strip_control_chars(username),
            primary_email=email,
            email_addresses=[email],
            avatar_url="https://gravatar.com/avatar/%s" % email_hash
        )
        return instance