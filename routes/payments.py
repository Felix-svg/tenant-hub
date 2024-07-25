from flask import make_response, jsonify, request
from flask_restful import Resource
from models.payment import Payment
from models.apartment import Apartment
from config import db
from utils import role_required, not_found, no_input_data, missing_fields, server_error
from flask_jwt_extended import jwt_required, get_jwt_identity


class Payments(Resource):
    @jwt_required()
    @role_required('manager')
    def get(self):
        try:
            manager_id = get_jwt_identity()

            # Get all apartments managed by the current manager
            apartments = Apartment.query.filter_by(manager_id=manager_id).all()
            apartment_ids = [apartment.id for apartment in apartments]

            # Get all payments associated with these apartments
            payments = Payment.query.filter(Payment.apartment_id.in_(apartment_ids)).all()

            payments_dict = [payment.to_dict(rules=['-lease']) for payment in payments]
            return make_response(jsonify({'payments': payments_dict}), 200)
        except Exception as e:
            return server_error(e)

    @jwt_required()
    @role_required('manager')
    def post(self):
        try:
            data = request.get_json()
            if not data:
                return no_input_data()

            lease_id = data.get('lease_id')
            amount = data.get('amount')
            payment_date = data.get('payment_date')

            if not lease_id or not amount or not payment_date:
                return missing_fields()

            new_payment = Payment(lease_id=lease_id, amount=amount, payment_date=payment_date)
            db.session.add(new_payment)
            db.session.commit()

            return make_response(jsonify({'message': 'Payment created successfully'}), 201)
        except Exception as e:
            db.session.rollback()
            return server_error(e)


class PaymentByID(Resource):
    @jwt_required()
    @role_required('manager')
    def get(self, id):
        try:
            manager_id = get_jwt_identity()

            payment = Payment.query.filter(Payment.id == id).first()
            if not payment:
                return not_found('Payment')

            # Check if the payment is associated with an apartment managed by the current manager
            apartment = Apartment.query.filter_by(id=payment.apartment_id, manager_id=manager_id).first()
            if not apartment:
                return make_response(jsonify({"error": "Access denied"}), 403)

            payment_dict = payment.to_dict()
            return make_response(jsonify({'payment': payment_dict}), 200)
        except Exception as e:
            return server_error(e)

    @jwt_required()
    @role_required('manager')
    def patch(self, id):
        try:
            payment = Payment.query.filter(Payment.id == id).first()
            if not payment:
                return not_found('Payment')

            data = request.get_json()
            if not data:
                return no_input_data()

            lease_id = data.get('lease_id')
            amount = data.get('amount')
            payment_date = data.get('payment_date')

            if lease_id is not None:
                payment.lease_id = lease_id

            if amount is not None:
                payment.amount = amount

            if payment_date is not None:
                payment.payment_date = payment_date

            db.session.commit()
            return make_response(jsonify({'message': 'Payment updated successfully'}), 200)
        except Exception as e:
            db.session.rollback()
            return server_error(e)

    @jwt_required()
    @role_required('manager')
    def delete(self, id):
        try:
            payment = Payment.query.filter(Payment.id == id).first()
            if not payment:
                return not_found('Payment')

            db.session.delete(payment)
            db.session.commit()

            return make_response(jsonify({'message': 'Payment deleted successfully'}), 200)
        except Exception as e:
            db.session.rollback()
            return server_error(e)
