from config import db
from sqlalchemy_serializer import SerializerMixin


class Payment(db.Model, SerializerMixin):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    lease_id = db.Column(db.Integer, db.ForeignKey('lease.id'))
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.Date, nullablee=False, server_default=db.func.now())

    buildings = db.relationship('Building', back_populates='payment')

    def __repr__(self):
        return f'Payment amount: {self.amount}'

