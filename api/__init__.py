import os
from flask_restful import Api
from flask_pymongo import PyMongo
from flask import make_response, Flask
from bson.json_util import dumps
import logging
import logging.handlers

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024 #1MB
app.debug = False

MONGO_URL = os.environ.get('MONGO_URL')
if not MONGO_URL:
    MONGO_URL = "mongodb://localhost:27017/test"; # give local url

app.config['MONGO_URI'] = MONGO_URL

GEO_URL = os.environ.get('GEO_URL')
if not GEO_URL:
    GEO_URL = "https://maps.googleapis.com/maps/api/geocode/json?&latlng="

app.config['GEO_URL'] = GEO_URL

mongo = PyMongo(app)

def output_json(obj, code, headers=None):
    resp = make_response(dumps(obj), code)
    resp.headers.extend(headers or {})
    return resp

api = Api(app)
api.representations = {'application/json': output_json}

# Logging section
handler = logging.FileHandler(os.environ.get("LOGFILE", "darpun.log"))
formatter = logging.Formatter("[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s")
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.WARNING)
logger.addHandler(handler)

import api.rest
