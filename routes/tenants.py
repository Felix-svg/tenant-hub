from flask import make_response, jsonify, request
from flask_restful import Resource
from models.tenant import Tenant
from config import db
from utils import role_required, not_found, no_input_data, server_error, missing_fields
from flask_jwt_extended import jwt_required, get_jwt_identity


class Tenants(Resource):
    @jwt_required()
    @role_required('manager')
    def get(self):
        try:
            manager_id = get_jwt_identity()
            tenants = [tenant.to_dict(rules=['-apartment', '-manager']) for tenant in Tenant.query.filter_by(manager_id==manager_id.all())]
            return make_response(jsonify({'tenants': tenants}), 200)
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
            email = data.get('email')
            phone_number = data.get('phone_number')
            password = data.get('password')
            apartment_id = data.get('apartment_id')
            manager_id = data.get('manager_id')

            if not all([name, email, phone_number, apartment_id, manager_id, password]):
                return missing_fields()

            new_tenant = Tenant(name=name, email=email, phone_number=phone_number, apartment_id=apartment_id, manager_id=manager_id)
            new_tenant.set_password(password)

            db.session.add(new_tenant)
            db.session.commit()

            return make_response(jsonify({'message': 'Tenant created successfully'}), 201)
        except Exception as e:
            db.session.rollback()
            return server_error(e)


class TenantByID(Resource):
    @jwt_required()
    @role_required('manager')
    def get(self, id):
        try:
            manager_id = get_jwt_identity()
            tenant = Tenant.query.filter_by(id=id, manager_id=manager_id).first()
            if not tenant:
                return not_found('Tenant')

            tenant_dict = tenant.to_dict(rules=['-apartment', '-manager'])
            return make_response(jsonify({'tenant': tenant_dict}), 200)
        except Exception as e:
            return server_error(e)


    @jwt_required()
    @role_required('manager')
    def patch(self, id):
        try:
            tenant = Tenant.query.filter(Tenant.id == id).first()
            if not tenant:
                return not_found('Tenant')

            data = request.get_json()
            if not data:
                return no_input_data()

            name = data.get('name')
            email = data.get('email')
            phone_number = data.get('phone_number')
            password = data.get('password')
            apartment_id = data.get('apartment_id')
            manager_id = data.get('manager_id')

            if name is not None:
                tenant.name = name

            if email is not None:
                tenant.email = email

            if phone_number is not None:
                tenant.phone_number = phone_number

            if password is not None:
                tenant.set_password(password)

            if apartment_id is not None:
                tenant.apartment_id = apartment_id

            if manager_id is not None:
                tenant.manager_id = manager_id

            db.session.commit()
            return make_response(jsonify({'message': 'Tenant updated successfully'}), 200)

        except Exception as e:
            db.session.rollback()
            return server_error(e)

    @jwt_required()
    @role_required('manager')
    def delete(self, id):
        try:
            tenant = Tenant.query.filter(Tenant.id == id).first()
            if not tenant:
                return not_found('Tenant')

            db.session.delete(tenant)
            db.session.commit()
            return make_response(jsonify({'message': 'Tenant deleted successfully'}), 200)
        except Exception as e:
            db.session.rollback()
            return server_error(e)
