import urllib

from flask import abort
from flask_restplus import Resource
from flask_restplus import fields
from flask_restplus import abort

from webapp.utils import AttributeHider
from webapp.api.oauth import oauth
from webapp.api.oauth import AuthorizationRequired
from webapp.api.blueprint import api
from webapp.api.models import podcast_full_fields
from webapp.podcasts import Podcast


ns = api.namespace("podcasts")

@ns.route("/p/<path:podcastId>", endpoint="podcast")
@api.doc(params={"podcastId":"A podcast's id (the same as its URL. If the API returns a podcast with a different URL, it means the podcast has moved."})
class PodcastResource(Resource):
    @api.marshal_with(podcast_full_fields)
    @api.doc(id="getPodcast")
    def get(self, podcastId):
        podcastId = urllib.unquote(podcastId)
        podcast = Podcast.get_by_url(podcastId)
        if podcast == None:
            abort(404, message="Podcast not found: %s" % podcastId)
        return podcast