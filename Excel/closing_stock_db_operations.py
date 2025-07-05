from models import MonthlyProductData
from database import db


def insert_monthly_product_data(month, year, product_dict):
    try:
        for product_name, values in product_dict.items():
            if not isinstance(values, list) or len(values) < 2:
                continue  # or raise an error

            quantity = values[0]
            bottles = values[1]

            entry = MonthlyProductData(
                month=month,
                product_name=product_name,
                quantity=quantity,
                bottles=bottles,
                year=year,
            )
            db.session.add(entry)

        db.session.commit()

        # 🔍 Debug: fetch what's in the DB after commit
        inserted = db.session.query(MonthlyProductData).filter_by(month=month).all()
        print(f"Inserted {len(inserted)} row(s):")
        for row in inserted:
            print(row.product_name, row.quantity, row.bottles)

        print(f"{len(product_dict)} products inserted for month: {month}")
        return {"count": len(inserted), "message": "Data inserted"}

    except Exception as e:
        db.session.rollback()
        return {"error": "Failed to insert data", "message": str(e)}


def get_product_data_by_month(month, year):
    entries = MonthlyProductData.query.filter_by(month=month, year=year).all()
    return [
        {
            "product": entry.product_name,
            "quantity": entry.quantity,
            "bottles": entry.bottles,
        }
        for entry in entries
    ]
