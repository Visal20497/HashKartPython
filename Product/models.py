from app import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    brand = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(25), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(32), nullable=False)