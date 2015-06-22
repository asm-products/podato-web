from flask import request
from flask_oauthlib.contrib.apps import facebook, google, twitter
from flask_oauthlib.client import OAuth

def _make_token_getter(provider):
    def token_getter():
        user = request.oauth.user
        return (user.get_provider_token(provider), "")
    return token_getter

oauth = OAuth()

facebook = facebook.register_to(oauth, scope=["public_profile", "email"])
facebook.tokengetter(_make_token_getter("facebook"))

google = google.register_to(oauth, scope=["https://www.googleapis.com/auth/plus.profile.emails.read"])
google.tokengetter(_make_token_getter("google"))

twitter = twitter.register_to(oauth)
twitter.tokengetter(_make_token_getter("twitter"))

def get_provider(provider):
    """Returns the requested identity provider or None if it doesn't exist."""
    return {
        "facebook": facebook,
        "google": google,
        "twitter": twitter
    }.get(provider)
