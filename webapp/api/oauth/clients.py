import logging

from db import db, Model

from flask import current_app
from flask import url_for

import utils

# Our own web application will be stored here.
PODATO_APP = None

# Trusted clients will be stored here.
TRUSTED_CLIENTS = {}


def _split_lines(t):
    if isinstance(t, list):
        return t
    lines = map(strip, t.split('\n'))


class Application(Model):
    """An application that would like to integrate with us.
    One application can have multiple clients."""
    name = db.StringField(primary_key=True)
    logo_url = db.URLField()
    contact_email = db.EmailField()
    homepage_url = db.URLField()
    privacy_policy_url = db.URLField()
    trusted = db.BooleanField(default=False)

    clients = db.ListField(db.ReferenceField("Client", reverse_delete_rule=db.PULL))
    owners = db.ListField(db.ReferenceField("User", reverse_delete_rule=db.PULL))

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
            name=utils.strip_control_chars(name),
            logo_url=logo_url,
            contact_email=contact_email,
            homepage_url=homepage_url,
            privacy_policy_url=privacy_policy_url
        )

        if owner:
            instance.owners.append(owner)

        return instance

    def add_owner(self, owner):
        self.modify(push__owners=owner)

    def remove_owner(self, owner):
        self.modify(pull__owners=owner)

    def add_client(self, *args, **kwargs):
        """Adds a new client for this application."""
        client = Client.create(app, *args, **kwargs)
        client.save()
        self.modify(push__clients=client)
        return client

    def remove_client(self, client):
        """Removes the client from the application, and deletes it."""
        self.modify(pull__clients=client)
        client.delete()


class Client(db.Document):
    """A client that has credentials to communicate with us."""
    app = db.ReferenceField(Application, required=True, reverse_delete_rule=db.CASCADEA)
    name = db.StringField(required=True)

    is_confidential = db.BooleanField(default=True)
    client_secret = db.StringField(required=True)

    own_redirect_uris = db.ListField(db.URLField())
    javascript_origins = db.ListField(db.URLField())
    default_scopes = db.ListField(db.StringField())

    @property
    def redirect_uris(self):
        rv = self.own_redirect_uris
        if self.javascript_origins:
            for origin in self.javascript_origins:
                rv.append(url_for("api.javascript_endpoint", origin=origin, _external=True))
        return rv

    @property
    def client_type(self):
        if self.is_confidential:
            return 'confidential'
        return 'public'

    @property
    def client_id(self):
        return self.id

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
        instance = cls(app=app, name=utils.strip_control_chars(name),
                       own_redirect_uris=_split_lines(redirect_uris), id=id)
        instance.validate()
        instance.client_secret = secret or utils.generate_random_string()
        return instance


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
        client.javascript_origins = client_dict.get("JAVASCRIPT_ORIGINS")
        TRUSTED_CLIENTS[client_dict["CLIENT_ID"]] = client
    return TRUSTED_CLIENTS

_load_trusted_clients()