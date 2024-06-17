from sqlalchemy import ForeignKey
from Product.models import Product
from app import db


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(
        db.Integer, ForeignKey(Product.id), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
