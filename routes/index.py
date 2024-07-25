from flask import make_response, jsonify, send_from_directory
from flask_restful import Resource
from config import app
import os

class Index(Resource):
    def get(self):
        return make_response(jsonify({'message':'Tenant Hub API'}), 200)


# Route to serve favicon
class Favicon(Resource):
    def get(self):
        return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')