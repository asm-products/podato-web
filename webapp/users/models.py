import md5

from google.appengine.ext import ndb

from users import auth
import utils

class User(ndb.Model, auth.ProviderTokenHolder):
    username = ndb.StringProperty(required=True)
    primary_email = ndb.StringProperty(required=True)
    email_addresses = ndb.StringProperty(repeated=True)
    avatar_url = ndb.StringProperty()

    @classmethod
    def create(cls, username, email, avatar_url=None):
        email_hash = md5.md5(email).hexdigest()
        instance = cls(
            username=utils.strip_control_chars(username),
            primary_email=email,
            email_addresses=[email],
            avatar_url="https://gravatar.com/avatar/%s" % email_hash
        )
        instance.validate()
        return instance

    def validate(self):
        utils.validate_email(self.primary_email)

        if self.avatar_url:
            utils.validate_url(self.avatar_url, allow_hash=False)

