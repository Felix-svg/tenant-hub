from config import db
from sqlalchemy_serializer import SerializerMixin


class Apartment(db.Model, SerializerMixin):
    __tablename__ = 'apartments'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(10), unique=True, nullable=False)
    building_id = db.Column(db.Integer, db.ForeignKey('buildings.id'))
    rent_amount = db.Column(db.Float, nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('managers.id'))

    tenant = db.relationship('Tenant', back_populates='apartment')
    building = db.relationship('Building', back_populates='apartments')
    manager = db.relationship('Manager', back_populates='apartments')

    def __repr__(self):
        return f'<Apartment {self.id}>'
