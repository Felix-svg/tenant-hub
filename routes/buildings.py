from flask import make_response, jsonify, request
from flask_restful import Resource
from models.building import Building
from config import db
from utils import role_required, not_found, no_input_data, server_error, missing_fields
from flask_jwt_extended import jwt_required, get_jwt_identity


class Buildings(Resource):
    def get(self):
        try:
            buildings = [building.to_dict() for building in Building.query.all()]
            return make_response(jsonify({'buildings': buildings}), 200)
        except Exception as e:
            return server_error(e)

    @jwt_required()
    @role_required('manager')
    def post(self):
        try:
            data = request.get_json()
            if not data:
                return no_input_data()

            name = data.get('name')
            address = data.get('address')

            if not name or not address:
                return missing_fields()

            new_building = Building(name=name, address=address)
            db.session.add(new_building)
            db.session.commit()

            return make_response(jsonify({'message': 'Building created successfully'}), 201)
        except Exception as e:
            db.session.rollback()
            return server_error(e)


class BuildingByID(Resource):
    def get(self):
        try:
            building = Building.query.filter(Building.id == id).first()
            if not building:
                return not_found('Building')

            building_dict = building.to_dict()
            return make_response(jsonify({'building': building_dict}), 200)
        except Exception as e:
            return server_error(e)

    @jwt_required()
    @role_required('manager')
    def patch(self, id):
        try:
            building = Building.query.filter(Building.id == id).first()
            if not building:
                return not_found('Building')

            data = request.get_json()
            if not data:
                return no_input_data()

            name = data.get('name')

            if name is not None:
                building.name = name

            db.session.commit()
            return make_response(jsonify({'message': 'Building updated successfully'}), 200)
        except Exception as e:
            db.session.rollback()
            return server_error(e)

    @jwt_required()
    @role_required('manager')
    def delete(self, id):
        try:
            building = Building.query.filter(Building.id == id).first()
            if not building:
                return not_found('Building')

            db.session.delete(building)
            db.session.commit()

            return make_response(jsonify({'message':'Building deleted successfully'}), 200)
        except Exception as e:
            db.session.rollback()
            return server_error(e)


