from flask import abort
from flask_restplus import Resource
from flask_restplus import fields
from flask_restplus import abort

from webapp.api.blueprint import api
from webapp.api.models import success_status
from webapp.async import AsyncSuccess

ns = api.namespace("async")

@ns.route("/<string:asyncId>", endpoint="async")
@api.doc(params={"asyncId":"An id returned by an async API call."})
class PodcastResource(Resource):
    @api.marshal_with(success_status)
    @api.doc(id="getAsync")
    def get(self, asyncId):
        return AsyncSuccess.get(asyncId)