from flask import request
from flask_restplus import Resource
from flask_restplus import fields
from flask_restplus import abort

from utils import AttributeHider
from api.oauth import oauth
from api.oauth import AuthorizationRequired
from api.blueprint import api
from api.models import user_fields, subscribe_fields, podcast_fields, success_status
from users import User


ns = api.namespace("users")

@ns.route("/<string:userId>", endpoint="user")
@api.doc(params={"userId": "A user ID, or \"me\" without quotes, for the user associated with the provided access token."})
class UserResource(Resource):
    @api.marshal_with(user_fields)
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
        if not (valid and (userId == "me" or userId == req.user.key.id())):
            return AttributeHider(user, ["primary_email"])
        return user

podcastsParser = api.parser()
podcastsParser.add_argument(name="podcast", action="append", required=True, location="args")

@ns.route("/<string:userId>/subscriptions", endpoint="subscriptions")
@api.doc({"userId": "A user ID, or \"me\" without quotes, for the user associated with the provided access token.", "podcast":"a podcast feed url."})
class SubscriptionResource(Resource):
    @api.marshal_with(success_status)
    @api.doc(id="subscribe", security=[{"javascript":[]}, {"server":[]}], parser=podcastsParser)
    def post(self, userId):
        podcasts = podcastsParser.parse_args()["podcast"]
        if userId == "me":
            valid, req = oauth.verify_request([])
            if not valid:
                raise AuthorizationRequired()
            user = req.user
            for podcast in podcasts:
                user.subscribe_by_url(podcast)

            user.put()
            return {"success": True}

    @api.marshal_with(success_status)
    @api.doc(id="unsubscribe", parser=podcastsParser)
    def delete(self, userId):
        podcasts = podcastsParser.parse_args()["podcast"]
        if userId == "me":
            valid, req = oauth.verify_request([])
            if not valid:
                raise AuthorizationRequired()
            user = req.user
        else:
            user = User.get_by_id(userId)

        for podcast in podcasts:
            user.unsubscribe_by_url(podcast)
        user.put()
        return {"success": True}

    @api.marshal_with(podcast_fields, as_list=True)
    @api.doc(id="getSubscriptions", security=[{"javascript":[]}, {"server":[]}])
    def get(self, userId):
        if userId == "me":
            valid, req = oauth.verify_request([])
            if not valid:
                raise AuthorizationRequired()
            user = req.user
        else:
            user = User.get_by_id(userIdz)
        if not user:
            abort(404, message="User not found.")
        return user.get_subscriptions()