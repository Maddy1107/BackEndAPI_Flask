import datetime
from database import db


class MonthlyProductData(db.Model):
    __tablename__ = "monthly_product_data"

    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.String(20), nullable=False)
    year = db.Column(db.String(20), nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.String(50), nullable=False)
    bottles = db.Column(db.String(50), nullable=False)


class ProductRequest(db.Model):
    __tablename__ = "product_requests"

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    requested_at = db.Column(db.Date, default=datetime.date.today)
    received = db.Column(db.Boolean, default=False)
    received_at = db.Column(db.Date, nullable=True)
