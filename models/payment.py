from config import db
from sqlalchemy_serializer import SerializerMixin


class Payment(db.Model, SerializerMixin):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    lease_id = db.Column(db.Integer, db.ForeignKey('leases.id'))
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.Date, nullable=False, server_default=db.func.now())

    lease = db.relationship('Lease', back_populates='payment')

    def __repr__(self):
        return f'Payment amount: {self.amount}'

