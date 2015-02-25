from flask import Blueprint
from flask_restful import Api

errors = {
    "AuthorizationRequired": {
        "message": "OAuth authorization failed",
        "status": 410
    }
}

api_blueprint = Blueprint("api", __name__)
api = Api(api_blueprint, errors=errors)
