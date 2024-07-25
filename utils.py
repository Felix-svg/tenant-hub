from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.token_block_list import TokenBlocklist
from models.tenant import Tenant
from models.manager import Manager
from functools import wraps
from config import jwt


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
