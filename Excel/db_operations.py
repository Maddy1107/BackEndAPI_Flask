from models import MonthlyProductData
from database import db


def insert_monthly_product_data(month, product_dict):
    db.session.query(MonthlyProductData).filter_by(month=month).delete()

    for product_name, values in product_dict.items():
        if not isinstance(values, list) or len(values) < 2:
            continue  # or raise an error

        quantity = values[0]
        bottles = values[1]

        entry = MonthlyProductData(
            month=month, product_name=product_name, quantity=quantity, bottles=bottles
        )
        db.session.add(entry)

    print(f"{len(product_dict)} products inserted for month: {month}")


def get_product_data_by_month(month):
    entries = MonthlyProductData.query.filter_by(month=month).all()
    return [
        {
            "product": entry.product_name,
            "quantity": entry.quantity,
            "bottles": entry.bottles,
        }
        for entry in entries
    ]
