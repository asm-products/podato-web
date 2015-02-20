import logging

from google.appengine.ext import ndb
from google.appengine.api import mail

from flask import current_app

import utils

# Our own web application will be stored here.
PODATO_APP = None

# Trusted clients will be stored here.
TRUSTED_CLIENTS = {}


def _split_lines(t):
    if isinstance(t, list):
        return t
    lines = map(strip, t.split('\n'))


class Application(ndb.Model):
    """An application that would like to integrate with us.
    One application can have multiple clients."""

    logo_url = ndb.StringProperty()
    contact_email = ndb.StringProperty()
    homepage_url = ndb.StringProperty()
    privacy_policy_url = ndb.StringProperty()
    trusted = ndb.BooleanProperty(default=False)

    clients = ndb.KeyProperty(kind="Client", repeated=True)
    owners = ndb.KeyProperty(kind="User", repeated=True)

    @classmethod
    def create(cls, name, owner, logo_url=None, contact_email=None, homepage_url=None,
               privacy_policy_url=None,):
        """Creates a new application.

        arguments:
          - name: human-readable name
          - owner: a User who owns this application.
          - logo_url: an url to a logo image for this application.
          - contact_email: an email address that users can use to contact someone about this application.
          - homepage_url: the url of the application's homepage
          - privacy_policy_url: the url of the application's privacy policy."""
        instance = cls(
            id=utils.strip_control_chars(name),
            logo_url=logo_url,
            contact_email=contact_email,
            homepage_url=homepage_url,
            privacy_policy_url=privacy_policy_url
        )

        if owner:
            instance.owners.append(owner)

        instance.validate()
        return instance


    def validate(self):
        """Checks that all of this applicatio's properties are valid, raises a ValueError if not."""
        if self.logo_url:
            utils.validate_url(self.logo_url, allow_hash=False)
        if self.homepage_url:
            utils.validate_url(self.homepage_url, allow_hash=True)
        if self.contact_email:
            utils.validate_email(self.contact_email)

    def add_client(self, *args, **kwargs):
        """Adds a new client for this application."""
        client = Client.create(app, *args, **kwargs)
        client.put()
        self.clients.append[client.key]
        return client


class Client(ndb.Model):
    """A client that has credentials to communicate with us."""
    app_key = ndb.KeyProperty(Application, required=True)
    name = ndb.StringProperty(required=True)

    is_confidential = ndb.BooleanProperty(default=True)
    client_secret = ndb.StringProperty(required=True)

    redirect_uris = ndb.StringProperty(repeated=True)
    default_scopes = ndb.StringProperty(repeated=True)

    @property
    def app(self):
        return self.app_key.get()

    @property
    def client_type(self):
        if self.is_confidential:
            return 'confidential'
        return 'public'

    @property
    def client_id(self):
        return self.key.string_id()

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @property
    def allowed_grant_types(self):
        grants = ["authorization_code", "refresh_token"]
        if self.app.trusted:
            grants.append("password")
        return grants

    @classmethod
    def create(cls, app, name, redirect_uris, id=None, secret=None):
        """Creates a new Client. Don't call this method directly, rather call
        Application.add_client."""
        instance = cls(app_key=app.key, name=utils.strip_control_chars(name),
                       redirect_uris=_split_lines(redirect_uris), id=id)
        instance.validate()
        instance.client_secret = secret or utils.generate_random_string()
        return instance

    def validate(self):
        """Checks that all this Client's properties are valid, raises a ValueError if not."""
        for uri in self.redirect_uris:
            utils.validate_url(uri, allow_hash=False)


    @classmethod
    def get_by_id(cls, id):
        """Gets the Client with the given id."""
        # Overriding this to return trusted clients.
        logging.debug("Retrieving client with id %s (trusted: %s)" % (id, id in TRUSTED_CLIENTS))
        return TRUSTED_CLIENTS.get(id) or super(Client, cls).get_by_id(id)


def _create_trusted_app():
    """Creates our own "Podato" app."""
    podato = Application.get_by_id("podato")
    if not podato:
        podato = Application.create("podato", None)
        podato.trusted = True
        podato.put()
    return podato


def _load_trusted_clients():
    global PODATO_APP
    if TRUSTED_CLIENTS:
        return TRUSTED_CLIENTS

    if not PODATO_APP:
        PODATO_APP = _create_trusted_app()

    trusted_clients = current_app.config.get("TRUSTED_CLIENTS")
    for client_dict in trusted_clients:
        client = Client.create(PODATO_APP,
                            client_dict["NAME"],
                            client_dict["REDIRECT_URLS"],
                            id=client_dict["CLIENT_ID"],
                            secret=client_dict["CLIENT_SECRET"])
        client.default_scopes = current_app.config.get("OAUTH_SCOPES").keys()
        TRUSTED_CLIENTS[client_dict["CLIENT_ID"]] = client
    return TRUSTED_CLIENTS

_load_trusted_clients()