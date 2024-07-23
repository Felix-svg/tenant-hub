from config import db
from sqlalchemy_serializer import SerializerMixin


class Building(db.Model, SerializerMixin):
    __tablename__ = 'buildings'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    apartments = db.relationship('Apartment', back_populates='building')

    def __repr__(self):
        return f'<{self.name}, Location: {self.address}>'


