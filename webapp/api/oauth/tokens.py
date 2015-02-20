import datetime

from google.appengine.ext import ndb

import utils


class GrantToken(ndb.Model):
    """Grant token, to be exchanged for a BearerToken."""
    _use_datastore = False # only store in cache.

    client_id = ndb.StringProperty(required=True)
    user = ndb.KeyProperty(required=True)
    redirect_uri = ndb.StringProperty(required=True)
    scopes = ndb.StringProperty(repeated=True)
    expires = ndb.DateTimeProperty(required=True)
    code = ndb.StringProperty(required=True)

    @classmethod
    def create(cls, client_id, code, user, redirect_uri, scopes):
        expires = datetime.datetime.utcnow() + datetime.timedelta(seconds=120)
        instance = cls(
            client_id=client_id,
            user=user.key,
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


class BearerToken(ndb.Model):
    """Token that clients can use to access resources."""
    refresh_token = ndb.StringProperty()
    client_key = ndb.KeyProperty(required=True)
    user_key = ndb.KeyProperty(required=True)
    scopes = ndb.StringProperty(repeated=True)
    expires = ndb.DateTimeProperty(required=True)
    token_type = ndb.StringProperty(required=True)

    @property
    def client_id(self):
        return self.client_key.id()

    @property
    def access_token(self):
        return self.key.id()

    @property
    def user(self):
        return self.user_key.get()

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

    def delete(self):
        self.key.delete()
