from flask_oauthlib.provider import OAuth2Provider

from flask import current_app


oauth = OAuth2Provider(current_app)
