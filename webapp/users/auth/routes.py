import os
import urlparse

from flask import request
from flask import url_for
from flask import redirect
from flask import render_template
from flask import abort

import webapp.cache
from webapp.users.blueprint import  users_blueprint
from webapp.users import models
from webapp.users.auth.providers import get_provider
from webapp.users.auth import session
from webapp.users.auth import errors



def _validate_next(next):
    """next must be a relative url, or its host must match the host where the request is running."""
    parsed = urlparse.urlparse(next)
    if parsed.netloc and parsed.netloc != request.host:
        raise errors.AuthError("Can't redirect to an absolute url after login. (%s is absolute.)" % next)

def _save_next(next):
    key = os.urandom(16).encode("hex")
    cache.set(key, next, 600)
    return key


def _get_next(key):
    return cache.get(key)


@users_blueprint.route("/login")
def login():
    next = request.args.get("next")
    return render_template("login.html", next=next)


@users_blueprint.route("/login/<provider>")
def provider_login(provider):
    # The next_token doesn't only store the 'next' value, but it also acts as a CSRF token.
    next = request.args.get("next") or "/"
    next_token = _save_next(next)

    provider_instance = get_provider(provider)
    if not provider_instance:
        abort(404)

    return provider_instance.authorize(callback=url_for("auth.authorized", _external=True, provider=provider), state=next_token)


@users_blueprint.route("/authorized/<provider>")
def authorized(provider):
    provider_instance = get_provider(provider)
    if not provider_instance:
        abort(404)

    resp = provider_instance.authorized_response()
    next = _get_next(request.args.get("state"))
    _validate_next(next)
    user = models.User.login(provider, resp)
    session.create_session_token(user)
    return redirect(next)
