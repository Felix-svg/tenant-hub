from flask import make_response, jsonify, request
from flask_restful import Resource
from models.lease import Lease
from config import db
from utils import role_required, not_found, no_input_data, server_error, missing_fields
from flask_jwt_extended import jwt_required, get_jwt_identity


class Leases(Resource):
    def get(self):
        try:
            leases = [lease.to_dict(rules=['-payment']) for lease in Lease.query.all()]
            return make_response(jsonify({'leases': leases}), 200)
        except Exception as e:
            return server_error(e)
    def post(self):
        try:
            data = request.get_json()
            if not data:
                return no_input_data()

            tenant_id = data.get('tenant_id')
            apartment_id = data.get('apartment_id')
            start_date = data.get('start_date')
            end_date = data.get('end_date')

            if not tenant_id or not apartment_id or not start_date or not end_date:
                return missing_fields()

            new_lease = Lease(tenant_id=tenant_id, apartment_id=apartment_id, start_date=start_date, end_date=end_date)
            db.session.add(new_lease)
            db.session.commit()
            return make_response(jsonify({'message': 'Lease created successfully'}), 201)

        except Exception as e:
            db.session.rollback()
            return server_error(e)


class LeaseByID(Resource):
    def get(self, id):
        try:
            lease = Lease.query.filter(Lease.id == id).first()
            if not lease:
                return not_found('Lease')

            lease_dict = lease.to_dict(rules=['-payment'])
            return make_response(jsonify({'lease': lease_dict}), 200)
        except Exception as e:
            return server_error(e)

    @jwt_required()
    @role_required('tenant')
    def patch(self, id):
        try:
            lease = Lease.query.filter(Lease.id == id).first()
            if not lease:
                return not_found('Lease')

            data = request.get_json()
            if not data:
                return no_input_data()

            tenant_id = data.get('tenant_id')
            apartment_id = data.get('apartment_id')
            start_date = data.get('start_date')
            end_date = data.get('end_date')

            if tenant_id is not None:
                lease.tenant_id = tenant_id

            if apartment_id is not None:
                lease.apartment_id = apartment_id

            if start_date is not None:
                lease.start_date = start_date

            if end_date is not None:
                lease.end_date = end_date

            db.session.commit()
            return make_response(jsonify({'message': 'Lease updated successfully'}),200)
        except Exception as e:
            db.session.rollback()
            return server_error(e)

    def delete(self, id):
        try:
            lease = Lease.query.filter(Lease.id == id).first()
            if not lease:
                return not_found('Lease')

            db.session.delete(lease)
            db.session.commit()

            return make_response(jsonify({'message': 'Lease deleted successfully'}), 200)
        except Exception as e:
            db.session.rollback()
            return server_error(e)

