from flask import current_app
from flask_oauthlib.provider import OAuth2Provider

from api.oauth import clients
from api.oauth import tokens
from api.oauth.oauth import oauth

from users import User
from users.auth import session

@oauth.clientgetter
def load_client(client_id):
    return clients.Client.get_by_id(client_id)

@oauth.grantgetter
def load_grant(client_id, code):
    return tokens.GrantToken.lookup(client_id, code)


@oauth.grantsetter
def save_grant(client_id, code, request, *args, **kwargs):
    grant = tokens.GrantToken.create(client_id, code["code"], session.get_user(),
                                     request.redirect_uri, request.scopes)
    return grant


@oauth.tokengetter
def load_token(access_token=None, refresh_token=None):
    if access_token:
        return tokens.BearerToken.get_by_id(access_token)
    else:
        return tokens.BearerToken.query(tokens.BearerToken.refresh_token == refresh_token).get()

@oauth.tokensetter
def save_token(token, request):
    tokens.BearerToken.create(
        client=request.client,
        user=session.get_user(),
        access_token=token["access_token"],
        refresh_token=token.get("refresh_token"),
        expires_in=token["expires_in"],
        scopes=token["scope"].split(),
        token_type=token["token_type"]
    ).put()

@oauth.usergetter
def get_user(platform, code, *args, **kwargs):
    user = User.create(username="bob", email="frederikcreemers@gmail.com", avatar_url="http://example.com")
    user.put()
    return user

import routes




