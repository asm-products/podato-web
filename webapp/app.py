import modify_pythonpath
import flask
import flask_restful

app = flask.Flask(__name__)
api = flask_restful.Api(app, prefix='/api')

#DeleteMe: This is just for testing that everything works.
class TestResource(flask_restful.Resource):
    def get(self, name):
        return {'hello': name}



api.add_resource(TestResource, '/<string:name>')
