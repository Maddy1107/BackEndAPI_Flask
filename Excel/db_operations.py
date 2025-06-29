from models import MonthlyProductData
from database import db


def insert_monthly_product_data(month, product_dict):
    db.session.query(MonthlyProductData).filter_by(month=month).delete()

    for product_name, quantity in product_dict.items():
        entry = MonthlyProductData(
            month=month, product_name=product_name, quantity=quantity
        )
        db.session.add(entry)
    db.session.commit()
    print(f"{len(product_dict)} products inserted for month: {month}")


def get_product_data_by_month(month):
    entries = MonthlyProductData.query.filter_by(month=month).all()
    return [
        {"product": entry.product_name, "quantity": entry.quantity} for entry in entries
    ]
