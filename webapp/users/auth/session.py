import os
from flask import session

import cache

from users.models import User
import errors


def create_session_token(user):
    token = os.urandom(16).encode("hex")
    cache.set("session-" + token, user.key.id(), 600)
    session["user_id"] = user.key.id()
    session["token"] = token


def get_user():
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