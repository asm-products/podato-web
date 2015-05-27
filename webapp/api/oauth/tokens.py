import datetime

from webapp.db import db, Model
from webapp.users import User
from clients import Client

from webapp import utils


class GrantToken(Model):
    """Grant token, to be exchanged for a BearerToken."""

    client_id = db.StringField(required=True)
    user = db.ReferenceField(User, required=True)
    redirect_uri = db.URLField(required=True)
    scopes = db.ListField(db.StringField())
    expires = db.DateTimeField(required=True)
    code = db.StringField(required=True)

    @classmethod
    def create(cls, client_id, code, user, redirect_uri, scopes):
        expires = datetime.datetime.utcnow() + datetime.timedelta(seconds=120)
        instance = cls(
            client_id=client_id,
            user=user,
            redirect_uri=redirect_uri,
            scopes=scopes,
            expires=expires,
            code=code,
            id=cls.make_id(client_id, code)
        )
        instance.put()
        return instance

    @classmethod
    def make_id(cls, client_id, code):
        return "%s-%s" % (client_id, code)

    @classmethod
    def lookup(cls, client_id, code):
        return cls.get_by_id(cls.make_id(client_id, code))


class BearerToken(Model):
    """Token that clients can use to access resources."""
    refresh_token = db.StringField()
    client = db.ReferenceField(Client, reverse_delete_rule=db.CASCADE)
    user = db.ReferenceField(User, reverse_delete_rule=db.CASCADE, required=True)
    scopes = db.ListField(db.StringField())
    expires = db.DateTimeField(required=True)
    token_type = db.StringField(required=True)

    @property
    def client_id(self):
        return self.client.id

    @property
    def access_token(self):
        return self.id

    @classmethod
    def create(cls, access_token, refresh_token, client, user, expires_in,
               token_type, scopes):
        """Create a new bearer token.

        arguments:
         - access_token: the access token
         - refresh_token: the refresh token
         - client: the Client object that can use this token
         - user: the User object, who has granted access to the client
         - expires_in: the number of seconds until this token expires
         - token_type: the token type.
         - scopes: a list of scopes.
         """
        expires = datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
        return cls(id=access_token,
                   refresh_token=refresh_token,
                   client_key=client.key,
                   user_key=user.key,
                   token_type=token_type,
                   scopes=scopes,
                   expires=expires)