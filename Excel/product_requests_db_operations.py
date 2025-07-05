from collections import defaultdict
from models import ProductRequest
from database import db
import datetime


def create_product_requests(product_list):
    today = datetime.date.today()

    for item in product_list:
        name = item.get("product_name")

        if not name:
            continue

        # 🧠 Check if a request for this product exists for today
        existing = ProductRequest.query.filter(
            ProductRequest.product_name == name,
            db.func.date(ProductRequest.requested_at) == today
        ).first()

        if existing:
            # 🔄 Overwrite logic: reset 'received' to False and clear 'received_at'
            existing.received = False
            existing.received_at = None
            existing.requested_at = datetime.date
        else:
            # ➕ Add new
            req = ProductRequest(product_name=name)
            db.session.add(req)

    db.session.commit()
    return {"message": "Products requested", "count": len(product_list)}


def get_all_product_requests():
    requests = ProductRequest.query.order_by(ProductRequest.requested_at.desc()).all()

    grouped = defaultdict(list)

    for r in requests:
        request_date = r.requested_at.date().isoformat()  # 'YYYY-MM-DD'
        grouped[request_date].append(
            {
                "id": r.id,
                "product_name": r.product_name,
                "received": r.received,
                "requested_at": r.requested_at,
                "received_at": r.received_at,
            }
        )

    # Convert dict to list format
    result = []
    for date, items in grouped.items():
        result.append({"date": date, "requests": items})

    return result


def mark_product_request_received(req_id):
    req = ProductRequest.query.get(req_id)
    if not req:
        return None

    req.received = True
    req.received_at = datetime.date
    db.session.commit()
    return req
