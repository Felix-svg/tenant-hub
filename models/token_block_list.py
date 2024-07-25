from config import db
from sqlalchemy_serializer import SerializerMixin


class TokenBlocklist(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)