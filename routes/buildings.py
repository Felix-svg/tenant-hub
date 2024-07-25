from flask import make_response, jsonify, request
from flask_restful import Resource
from models.building import Building
from models.apartment import Apartment
from config import db
from utils import role_required, not_found, no_input_data, server_error, missing_fields, get_jwt_role
from flask_jwt_extended import jwt_required, get_jwt_identity


class Buildings(Resource):
    @jwt_required()
    @role_required('manager')
    def get(self):
        try:
            manager_id = get_jwt_identity()
            # Get buildings that have apartments managed by the manager
            buildings = db.session.query(Building).join(Apartment).filter(Apartment.manager_id == manager_id).all()
            buildings_dict = [building.to_dict() for building in buildings]
            return make_response(jsonify({'buildings': buildings_dict}), 200)
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
    @jwt_required()
    def get(self, id):
        try:
            current_user_id = get_jwt_identity()
            current_user_role = get_jwt_role()

            # Fetch the building by ID
            building = Building.query.filter(Building.id == id).first()
            if not building:
                return not_found('Building')

            if current_user_role == 'manager':
                # Check if the building has any apartments managed by the current manager
                apartments = Apartment.query.filter_by(manager_id=current_user_id, building_id=id).all()
                if not apartments:
                    return jsonify({"error": "Access denied"}), 403

            # No additional checks needed for other roles

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
            address = data.get('address')

            if name is not None:
                building.name = name

            if address is not None:
                building.address = address

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
            return make_response(jsonify({'message': 'Building deleted successfully'}), 200)
        except Exception as e:
            db.session.rollback()
            return server_error(e)
