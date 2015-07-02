import functools
import os
from flask import session
from flask import url_for
from flask import redirect
from flask import request

from webapp import cache

from webapp.users.models import User
import errors


def create_session_token(user):
    """Creates a new session token, and stores it on the session."""
    token = os.urandom(16).encode("hex")
    cache.set("session-" + token, str(user.id), 600)
    session["user_id"] = str(user.id)
    session["token"] = token


def destroy_session():
    """Destroys the current user session."""
    session.clear()


def get_user():
    """get the user for the current session."""
    token = session.get("token")
    user_id = session.get("user_id")

    if (not token) or (not user_id):
        return None

    cache_result = cache.get("session-" + token)
    if cache_result is None:
        return None

    if user_id != cache_result:
        raise errors.AuthError("The session isn't valid.")

    return User.get_by_id(user_id)

def require(f):
    """A decorator that you can add to a funciton to require a session to be present."""
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if not get_user():
            provider = request.args.get("provider")
            if provider:
                return redirect(url_for("auth.provider_login", provider=provider, next=request.url))
            return redirect(url_for("auth.login", next=request.url))
        return f(*args, **kwargs)
    return wrapper
