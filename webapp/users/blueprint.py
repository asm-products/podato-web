from flask import Blueprint

users_blueprint = Blueprint("auth", __name__, url_prefix="/auth")