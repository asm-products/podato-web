import logging

from flask import abort
from webapp.db import db

from webapp.users.auth import facebook_api

class ProvidedIdentity(db.EmbeddedDocument):
    provider = db.StringField(required=True)
    user_id = db.StringField(required=True)
    access_token = db.StringField(required=True)


class ProviderTokenHolder(object):
    """This is one of User's superclasses, which stores the auth tokens of 3rd party providers like Facebook or Google"""

    provided_identities = db.EmbeddedDocumentListField(ProvidedIdentity)

    def add_provided_identity(self, provider, user_id, access_token):
        # If the user already has an identity from the given platform with the given id,
        # update its access_token
        for identity in self.provided_identities:
            if identity.provider == provider and identity.user_id == user_id:
                identity.access_token = access_token
                self.put
                return


        prid = ProvidedIdentity(
            provider="facebook",
            user_id=user_id,
            access_token=access_token
        )
        self.modify(push__provided_identities=prid)

    def get_provider_token(self, provider, user_id=None):
        for identity in self.provided_identities:
            if identity.provider == provider:
                if user_id == None or identity.user_id == user_id:
                    return identity.access_token
        return None

    @classmethod
    def get_by_provided_identity(cls, provider, user_id):
        """Gets the User associated with the given provided identity."""
        return cls.query(provided_identities__provider=provider, provided_identities__user_id=user_id).first()

    @classmethod
    def login(cls, provider, provider_response):
        """Get or create the user given the name of the auth provider, and the provider's response."""
        if not hasattr(cls, "login_%s" % provider):
            abort(404)
        return getattr(cls, "login_%s" % provider)(provider_response)

    @classmethod
    def login_facebook(cls, facebook_response):
        """Gets or creates a user, based on the facebook_response."""
        access_token = facebook_response["access_token"]
        fb_user = facebook_api.get_current_user(access_token)
        user = cls.get_by_provided_identity("facebook", fb_user["id"])
        if not user:
            user = cls.create(fb_user["name"], fb_user["email"], facebook_api.get_avatar(fb_user["id"]))
            user.put()
        user.add_provided_identity("facebook", fb_user["id"], access_token)
        return user
