import modify_pythonpath
import flask
import flask_restful

from config import settings

app = flask.Flask(__name__)
app.config.from_object(settings)

with app.app_context():
    from users import users_blueprint
    from api import api_blueprint

    app.register_blueprint(users_blueprint, url_prefix="/auth")
    app.register_blueprint(api_blueprint, url_prefix="/api")