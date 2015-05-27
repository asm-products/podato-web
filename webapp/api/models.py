from webapp.api.blueprint import api
from flask_restplus import fields

id_field = api.model("id", {
    "id": fields.String
})

success_status = api.model("success_status", {
    "success": fields.Boolean
})

user_fields = api.extend("user", id_field, {
    "username": fields.String,
    "avatar_url": fields.String,
    "email_address": fields.String(attribute="primary_email")
})

subscribe_fields = api.model("subscribe", {
    "podcast": fields.String
})

podcast_fields = api.extend("podcast_simple", id_field, {
    "title": fields.String,
    "author": fields.String,
    "image": fields.String,
    "description": fields.String
})

class Duration(fields.Raw):
    def format(self, value):
        seconds = value % 60
        value = value-seconds
        minutes = (value % 3600)/60
        value = value-minutes*60
        hours = value / 3600

        if hours == 0:
            return "%s:%s" % (minutes, seconds)
        return "%s:%s:%s" % (hours, minutes, seconds)


class Explicit(fields.Raw):
    def format(self, value):
        return ["undefined", "clean", "explicit"][value]

enclosure_fields = api.model("enclosure", {
        "length": fields.Integer,
        "type": fields.String,
        "url": fields.String
})

episode_fields = api.extend("episode", podcast_fields, {
    "subtitle": fields.String,
    "duration": Duration,
    "summary": fields.String,
    "explicit": Explicit,
    "summary": fields.String,
    "guid": fields.String,
    "published": fields.DateTime,
    "enclosure": fields.Nested(enclosure_fields)
})

podcast_full_fields = api.extend("podcast_full", podcast_fields, {
    "copyright": fields.String,
    "language": fields.String,
    "complete": fields.Boolean,
    "episodes": fields.List(fields.Nested(episode_fields)),
})