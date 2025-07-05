from flask import request, jsonify

from Excel.closing_stock_db_operations import (
    insert_monthly_product_data,
    get_product_data_by_month,
)
from Excel.product_requests_db_operations import (
    create_product_requests,
    get_all_product_requests,
    mark_product_request_received,
)


def register_product_routes(app):
    @app.route("/month-data", methods=["POST"])
    def upload_month_data():
        month = request.args.get("month")
        year = request.args.get("year")
        data = request.get_json()

        if not month or not data:
            return (
                jsonify(
                    {"error": "Month (query) and product data (JSON body) required"}
                ),
                400,
            )

        try:
            insert_monthly_product_data(month, year, data)
            return jsonify({"message": "Data inserted", "count": len(data)})
        except Exception as e:
            return jsonify({"error": "Failed to insert data", "message": str(e)}), 500

    @app.route("/month-data/<month>", methods=["GET"])
    def fetch_month_data(month):
        year = request.args.get("year")
        if not year:
            return jsonify({"error": "Year (query) is required"}), 400
        data = get_product_data_by_month(month, year)
        return jsonify({"month": month, "year": year, "products": data})

    @app.route("/request-products", methods=["POST"])
    def request_products():
        data = request.get_json()
        if not isinstance(data, list):
            return jsonify({"error": "Expected a list of product requests"}), 400

        result = create_product_requests(data)
        return jsonify(result)

    @app.route("/requested-products", methods=["GET"])
    def get_requested_products():
        data = get_all_product_requests()
        return jsonify(data)

    @app.route("/mark-received/<int:req_id>", methods=["POST"])
    def mark_received(req_id):
        updated_request = mark_product_request_received(req_id)
        if not updated_request:
            return jsonify({"error": "Request not found"}), 404
        return jsonify({"message": "Marked as received", "id": updated_request.id})
