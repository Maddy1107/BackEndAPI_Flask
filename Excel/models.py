from database import db


class MonthlyProductData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.String(20), nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.String(50), nullable=False)
