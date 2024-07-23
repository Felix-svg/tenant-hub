from config import db
from sqlalchemy_serializer import SerializerMixin


class Lease(db.Model, SerializerMixin):
    __tablename__ = 'leases'

    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'))
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartments.id'))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    payments = db.relationship('Payment', back_populates='lease')

    def __repr__(self):
        return f'<Lease start date: {self.start_date}, Lease end date: {self.end_date}>'

