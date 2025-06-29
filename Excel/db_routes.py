from flask import request, jsonify
from db_operations import insert_month_data, get_month_data


def register_product_routes(app):
    @app.route("/month-data", methods=["POST"])
    def upload_month_data():
        month = request.args.get("month")
        data = request.get_json()

        if not month or not data:
            return (
                jsonify(
                    {"error": "Month (query) and product data (JSON body) required"}
                ),
                400,
            )

        try:
            insert_month_data(month, data)
            return jsonify({"message": "Data inserted", "count": len(data)})
        except Exception as e:
            return jsonify({"error": "Failed to insert data", "message": str(e)}), 500

    @app.route("/month-data/<month>", methods=["GET"])
    def fetch_month_data(month):
        data = get_month_data(month)
        return jsonify({"month": month, "products": data})
