from flask import make_response, jsonify, request
from flask_restful import Resource
from models.apartment import Apartment
from config import db
from utils import role_required
from flask_jwt_extended import jwt_required, get_jwt_identity


class Apartments(Resource):
    @jwt_required()
    @role_required('manager')
    def post(self):
        try:
            data = request.get_json()
            if not data:
                return make_response(jsonify({'error':'No input data provided'}), 400)

            number = data.get('number')
            building_id = data.get('building_id')
            rent_amount = data.get('rent_amount')
            manager_id = get_jwt_identity()

            if not number or not building_id or not rent_amount:
                return make_response(jsonify({'error':'Missing required fields'}), 400)

            new_apartment = Apartment(number=number, building_id=building_id, rent_amount=rent_amount, manager_id=manager_id)

            db.session.add(new_apartment)
            db.session.commit()

            return make_response(jsonify({'message':'Apartment created successfully'}), 201)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'error':'Internal Server Error: ' + str(e)}), 500)
    def get(self):
        try:
            apartments = [apartment.to_dict() for apartment in Apartment.query.all()]
            return make_response(jsonify({'apartments': apartments}), 200)
        except Exception as e:
            return make_response(jsonify({'error': 'Internal Server Error: ' + str(e)}), 500)


class ApartmentByID(Resource):
    def get(self, id):
        pass

    @jwt_required()
    def patch(self, id):
        pass

    @jwt_required()
    @role_required('manager')
    def delete(self, id):
        pass
