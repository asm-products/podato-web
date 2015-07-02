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
        """Creates a new GrantToken

        client_id: The id of the client to which this grant token was issued.
        code: The code associated with this token, used for lookup.
        user: The user who is asked to grant access.
        redirect_uri: the uri to be redirected to after access is granted
        scopes: the requested oauth scopes.
        """
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
        """A consistent way to make an id for a grant_token."""
        return "%s-%s" % (client_id, code)

    @classmethod
    def lookup(cls, client_id, code):
        """Looks up a grant token for the given client and code."""
        return cls.get_by_id(cls.make_id(client_id, code))


class BearerToken(Model):
    """Token that clients can use to access resources."""
    access_token = db.StringField(required=True, unique=True)
    refresh_token = db.StringField()
    client_id = db.StringField(required=True)
    user = db.ReferenceField(User, reverse_delete_rule=db.CASCADE, required=True)
    scopes = db.ListField(db.StringField())
    expires = db.DateTimeField(required=True)
    token_type = db.StringField(required=True)

    @property
    def client(self):
        return Client.get_by_id(self.client_id)

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
        return cls(access_token=access_token,
                   refresh_token=refresh_token,
                   client_id=client.client_id,
                   user=user,
                   token_type=token_type,
                   scopes=scopes,
                   expires=expires)