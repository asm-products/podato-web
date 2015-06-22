from flask import abort
from flask_restplus import Resource
from flask_restplus import fields
from flask_restplus import abort

from webapp.api.blueprint import api
from webapp.api.representations import success_status
from webapp.async import AsyncSuccess

ns = api.namespace("async")

@ns.route("/<string:asyncId>", endpoint="async")
@api.doc(params={"asyncId":"An id returned by an async API call."})
class AsyncResource(Resource):
    """Resource that represents the state of an asynchronously running job."""
    @api.marshal_with(success_status)
    @api.doc(id="getAsync")
    def get(self, asyncId):
        """Get the state of an async job by its id."""
        return AsyncSuccess.get(asyncId)