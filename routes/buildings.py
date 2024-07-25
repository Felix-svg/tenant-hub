from flask import make_response, jsonify, request
from flask_restful import Resource
from models.building import Building
from config import db
from utils import role_required
from flask_jwt_extended import jwt_required, get_jwt_identity


class Buildings(Resource):
    pass


class BuildingByID(Resource):
    pass


