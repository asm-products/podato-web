import md5

from webapp.db import db, Model

from webapp.users import auth
from webapp.podcasts import SubscriptionHolder
from webapp import utils

class User(Model, auth.ProviderTokenHolder, SubscriptionHolder):
    """Model that represents a user."""
    username = db.StringField(required=True, unique=True)
    primary_email = db.EmailField(required=True)
    email_addresses = db.ListField(db.EmailField())
    avatar_url = db.URLField()

    @classmethod
    def create(cls, username, email, avatar_url=None):
        """Create a new user with the given username, email and avatar url."""
        email_hash = md5.md5(email).hexdigest()
        instance = cls(
            username=utils.strip_control_chars(username),
            primary_email=email,
            email_addresses=[email],
            avatar_url=avatar_url or "https://gravatar.com/avatar/%s" % email_hash
        )
        return instance