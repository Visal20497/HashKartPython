from sqlalchemy import ForeignKey
from Cart.models import Cart
from app import db


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # product_id = db.Column(db.Integer, ForeignKey(Cart.id), nullable=False)
    amount= db.Column(db.Integer, nullable=False)
    currency=db.Column(db.String(50),nullable=False)
    session_id=db.Column(db.Integer)
    status=db.Column(db.String(30),nullable=False)
    created=db.Column(db.String(20),nullable=False)
    name=db.Column(db.String(30),nullable=False)
    email=db.Column(db.String(30),nullable=False)
