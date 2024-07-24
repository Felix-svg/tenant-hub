from config.config import db
from sqlalchemy_serializer import SerializerMixin


class Apartment(db.Model, SerializerMixin):
    __tablename__ = 'apartments'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10), unique=True, nullable=False)
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.id'))
    rent_amount = db.Column(db.Float, nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('managers.id'))
    tenants = db.relationship('Tenant', back_populates='apartment')

    def __repr__(self):
        return f'<Apartment {self.id}>'


