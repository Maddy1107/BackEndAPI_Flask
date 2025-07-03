from flask import request, jsonify
from db_operations import insert_monthly_product_data, get_product_data_by_month


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
