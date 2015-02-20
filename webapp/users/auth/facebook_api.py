"""Contains any functions that access the Facebook api"""
from users.auth.providers import facebook

API_VERSION = "v2.2"

def get_current_user(access_token=None):
    """Gets the facebook user associated with the logged in user, or the user
    associated with the given access_token."""
    return facebook.get("/%s/me" % API_VERSION, token=(access_token, "")).data

def get_avatar(user_id):
    """Gets the avatar of the facebook user with the given id."""
    return "https://"