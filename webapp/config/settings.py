import json
import os
import logging

data = json.load(open(os.path.join(os.path.dirname(__file__), "settings.json")))

for key, value in data.iteritems():
    locals()[key] = value

SERVER_NAME = os.environ.get("HTTP_HOST", "localhost") + ":" + os.environ["PORT"]
logging.error("SERVER_NAME: %s" % SERVER_NAME)