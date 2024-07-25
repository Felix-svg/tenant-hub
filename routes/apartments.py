from flask import make_response, jsonify, request
from flask_restful import Resource
from models.apartment import Apartment
from config import db
from utils import role_required, not_found, server_error, missing_fields, no_input_data
from flask_jwt_extended import jwt_required, get_jwt_identity


class Apartments(Resource):
    @jwt_required()
    @role_required('manager')
    def get(self):
        try:
            manager_id = get_jwt_identity()
            apartments = [apartment.to_dict(rules=['-building', '-manager', '-tenant']) for apartment in Apartment.query.filter_by(manager_id=manager_id).all()]
            return make_response(jsonify({'apartments': apartments}), 200)
        except Exception as e:
            return server_error(e)

    @jwt_required()
    @role_required('manager')
    def post(self):
        try:
            data = request.get_json()
            if not data:
                return no_input_data()

            number = data.get('number')
            building_id = data.get('building_id')
            rent_amount = data.get('rent_amount')
            manager_id = get_jwt_identity()

            if not number or not building_id or not rent_amount:
                return missing_fields()

            new_apartment = Apartment(number=number, building_id=building_id, rent_amount=rent_amount, manager_id=manager_id)

            db.session.add(new_apartment)
            db.session.commit()

            return make_response(jsonify({'message': 'Apartment created successfully'}), 201)
        except Exception as e:
            db.session.rollback()
            return server_error(e)


class ApartmentByID(Resource):
    def get(self, id):
        try:
            apartment = Apartment.query.filter(Apartment.id == id).first()
            if not apartment:
                return not_found('Apartment')

            apartment_dict = apartment.to_dict(rules=['-building', '-manager', '-tenant'])
            return make_response(jsonify({'apartment': apartment_dict}), 200)
        except Exception as e:
            return server_error(e)

    @jwt_required()
    @role_required('manager')
    def patch(self, id):
        try:
            apartment = Apartment.query.filter(Apartment.id == id).first()
            if not apartment:
                return not_found('Apartment')

            data = request.get_json()
            if not data:
                return no_input_data()

            number = data.get('number')
            rent_amount = data.get('rent_amount')

            if number is not None:
                apartment.number = number

            if rent_amount is not None:
                apartment.rent_amount = rent_amount

            db.session.commit()
            return make_response(jsonify({'message': 'Apartment updated successfully'}), 200)
        except Exception as e:
            db.session.rollback()
            return server_error(e)

    @jwt_required()
    @role_required('manager')
    def delete(self, id):
        try:
            apartment = Apartment.query.filter(Apartment.id == id).first()
            if not apartment:
                return not_found('Apartment')

            db.session.delete(apartment)
            db.session.commit()

            return make_response(jsonify({'message': 'Apartment deleted successfully'}), 200)
        except Exception as e:
            db.session.rollback()
            return server_error(e)
