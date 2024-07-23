from config import db, bcrypt
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin


class Manager(db.Model, SerializerMixin, UserMixin):
    __tablename__ = 'managers'

    id = db.Model(db.Integer, primary_key=True)
    name = db.Model(db.String(100), nullable=False)
    email = db.Column(db.String(120),nullable=False)
    phone_number = db.Model(db.String(15), nullable=False)
    password_hash = db.Model(db.String(128), nullable=False)
    tenants = db.relationship('Tenant', back_populates='manager')
    apartments = db.relationship('Apartment', back_populates='manager')

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.generate_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Name: {self.name}, Email: {self.email}>'

