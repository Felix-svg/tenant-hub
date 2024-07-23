from config import db, bcrypt
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin


class Tenant(db.Model, SerializerMixin, UserMixin):
    __tablename__ = 'tenants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.id'))
    manager_id = db.Column(db.Integer, db.ForeignKey('manager.id'))

    apartment = db.relationship('Apartment', back_populates='tenant')
    manager = db.relationship('Manager', back_populates='tenants')

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Name: {self.name}, Email: {self.email}>'

