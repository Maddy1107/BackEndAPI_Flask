from flask import request, jsonify
from app_factory import create_app

from db_routes import register_product_routes
from excel_routes import register_excel_routes

# ✅ Start with dummy dev app
app = create_app(env="development")

# ✅ Register routes
register_product_routes(app)
register_excel_routes(app)


@app.route("/set_env", methods=["POST"])
def set_env():
    global app
    data = request.get_json()
    env = data.get("build_type", "development").lower()

    if env not in ["development", "production"]:
        return jsonify({"error": "Invalid env"}), 400

    try:
        # ✅ Rebuild app with new env
        app = create_app(env=env)
        return jsonify({"message": f"Environment set to {env}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/debug/db", methods=["GET"])
def debug_db():
    return jsonify({"uri": app.config["SQLALCHEMY_DATABASE_URI"]})


@app.route("/warmup")
def warmup():
    try:
        from models import MonthlyProductData

        with app.app_context():
            item = MonthlyProductData.query.first()
            return jsonify({"ok": True, "data": item.to_dict() if item else None}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
