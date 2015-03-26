from flask import abort
from flask_restplus import Resource
from flask_restplus import marshal_with
from flask_restplus import fields

from utils import AttributeHider
from api.oauth import oauth
from api.oauth import AuthorizationRequired
from api.blueprint import api
from users import User

user_fields = {
    "username": fields.String,
    "avatar_url": fields.String,
    "email_address": fields.String(attribute="primary_email"),
    "id": fields.String
}

ns = api.namespace("users")


@ns.route("/<string:user_id>", endpoint="user")
@api.doc(params={"userId": "A user ID, or \"me\" without quotes, for the user associated with the provided access token."})
class UserResource(Resource):
    @marshal_with(user_fields)
    @api.doc(id="getUser", security=[{"javascript":[]}, {"server":[]}])
    def get(self, userId):
        if userId == "me":
            valid, req = oauth.verify_request(["publicuserinfo/read"])
            if not valid:
                raise AuthorizationRequired()
            user = req.user
        else:
            user = User.get_by_id(userId)

        if not user:
            abort(404, "No user with the given id.")

        # make sure the client is authorized to get the user's email.
        valid, req = oauth.verify_request(["userinfo/email"])
        if not (valid and (user_id == "me" or user_id == req.user.key.id())):
            return AttributeHider(user, ["primary_email"])
        return user
