import json
import os

data = json.load(open(os.path.join(os.path.dirname(__file__), "settings.json")))

for key, value in data.iteritems():
    locals()[key] = value