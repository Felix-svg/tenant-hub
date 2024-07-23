from config import db, bcrypt
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin

class User(db.Model, SerializerMixin, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String,unique=True, nullable=False)
    phone_number = db.Column(db.Integer, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartments.id'))
