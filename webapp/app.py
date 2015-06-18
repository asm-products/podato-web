import logging
import sys

import db
import cache
import flask
import flask_restful

from config import settings
from flask import request
from flask import redirect

app = flask.Flask(__name__)
app.config.from_object(settings)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
db.init_db(app)
cache.init_cache(app)

@app.before_request
def ensure_secure():
    if not request.is_secure and "localhost" not in request.host:
       redirect(request.url.replace("http", "https", 1), 301)

@app.after_request
def hsts(response):
    if "localhost" not in request.host:
        response.headers["Strict-Transport-Security"] = "max-age=31536000; preload"
    return response

with app.app_context():
    from users import users_blueprint
    from api import api_blueprint
    app.register_blueprint(users_blueprint)
    app.register_blueprint(api_blueprint)
