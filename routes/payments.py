from flask import make_response, jsonify, request
from flask_restful import Resource
from models.apartment import Apartment
from config import db
from utils import role_required
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.payment import Payment


class Payments(Resource):
    pass


class PaymentByID(Resource):
    pass