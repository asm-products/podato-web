from api.blueprint import api
from flask_restplus import fields

success_status = api.model("success_status", {
    "success": fields.Boolean
})

user_fields = api.model("user", {
    "username": fields.String,
    "avatar_url": fields.String,
    "email_address": fields.String(attribute="primary_email"),
    "id": fields.String
})

subscribe_fields = api.model("subscribe", {
    "podcast": fields.String
})

podcast_fields = api.model("podcast_simple", {
    "title": fields.String,
    "author": fields.String,
    "image": fields.String,
    "id": fields.String,
    "description": fields.String
})