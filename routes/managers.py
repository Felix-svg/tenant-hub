from flask import make_response, jsonify, request
from flask_restful import Resource
from models.manager import Manager
from config import db
from utils import role_required, no_input_data, not_found, server_error, missing_fields
from flask_jwt_extended import jwt_required, get_jwt_identity


class Managers(Resource):
    @jwt_required()
    @role_required('admin')
    def get(self):
        try:
            managers = [manager.to_dict(rules=['-tenants', '-apartments']) for manager in Manager.query.all()]
            return make_response(jsonify({'managers': managers}), 200)
        except Exception as e:
            return server_error(e)

    @jwt_required()
    @role_required('admin')
    def post(self):
        try:
            data = request.get_json()
            if not data:
                return no_input_data()

            name = data.get('name')
            email = data.get('email')
            phone_number = data.get('phone_number')
            password = data.get('password')
            role = data.get('role')

            if not all([name, email, phone_number, password, role]):
                return missing_fields()

            new_manager = Manager(name=name, email=email, phone_number=phone_number, role=role)
            new_manager.set_password(password)

            db.session.add(new_manager)
            db.session.commit()

            return make_response(jsonify({'message': 'Manager created successfully'}), 201)
        except Exception as e:
            db.session.rollback()
            return server_error(e)

class ManagerByID(Resource):
    @jwt_required()
    @role_required('admin')
    def get(self, id):
        try:
            manager = Manager.query.filter(Manager.id == id).first()
            if not manager:
                return not_found('Manager')

            manager_dict = manager.to_dict(rules=['-tenants', '-apartments'])
            return make_response(jsonify({'manager': manager_dict}), 200)
        except Exception as e:
            return server_error(e)

    @jwt_required()
    @role_required('admin')
    def patch(self, id):
        try:
            manager = Manager.query.filter(Manager.id == id).first()
            if not manager:
                return not_found('Manager')

            data = request.get_json()
            if not data:
                return no_input_data()

            name = data.get('name')
            email = data.get('email')
            phone_number = data.get('phone_number')
            password = data.get('password')

            if name is not None:
                manager.name = name

            if email is not None:
                manager.email = email

            if phone_number is not None:
                manager.phone_number = phone_number

            if password is not None:
                manager.set_password(password)

            db.session.commit()
            return make_response(jsonify({'message': 'Manager updated successfully'}), 200)
        except Exception as e:
            db.session.rollback()
            return server_error(e)

    @jwt_required()
    @role_required('admin')
    def delete(self, id):
        try:
            manager = Manager.query.filter(Manager.id == id).first()
            if not manager:
                return not_found('Manager')

            db.session.delete(manager)
            db.session.commit()
            return make_response(jsonify({'message': 'Manager deleted successfully'}), 200)
        except Exception as e:
            db.session.rollback()
            return server_error(e)
