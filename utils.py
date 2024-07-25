from flask import jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, create_access_token
from models.token_block_list import TokenBlocklist
from models.tenant import Tenant
from models.manager import Manager
from functools import wraps
from config import jwt


# def create_jwt_token(user):
#     additional_claims = {
#         'role': user.role
#     }
#     access_token = create_access_token(identity=user.id, additional_claims=additional_claims)
#     return access_token


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = TokenBlocklist.query.filter_by(jti=jti).first()
    return token is not None


def role_required(required_role):
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorated_view(*args, **kwargs):
            current_user_id = get_jwt_identity()
            user = Tenant.query.get(current_user_id)
            if user is None:
                # If not found, try the Manager model
                user = Manager.query.get(current_user_id)

            if user is None:
                # If still not found, return unauthorized
                return jsonify({"error": "User not found"}), 404

            if user.role != required_role:
                return jsonify({"error": "Access denied"}), 403
            return fn(*args, **kwargs)

        return decorated_view

    return wrapper


def get_jwt_role():
    claims = get_jwt()
    return claims.get('role', None)


def not_found(model_instance):
    return make_response(jsonify({'error': f'{model_instance} not found'}), 404)


def server_error(e):
    return make_response(jsonify({'error': 'Internal Server Error: ' + str(e)}), 500)


def missing_fields():
    return make_response(jsonify({'error': 'Missing required fields'}), 400)


def no_input_data():
    return make_response(jsonify({'error': 'No input data provided'}), 400)
