from flask import Flask, jsonify, request
from config_state import ConfigState
from database import init_db

from db_routes import register_product_routes
from excel_routes import register_excel_routes

app = Flask(__name__)

init_db(app)
register_excel_routes(app)
register_product_routes(app)


@app.route("/set_env", methods=["POST"])
def set_env():
    data = request.get_json()
    env = data["build_type"].lower() if "build_type" in data else "development"

    print(f"Setting environment to: {env}")
    if env not in ["development", "production"]:
        return jsonify({"error": "Invalid environment"}), 400

    ConfigState.current_env = env

    return jsonify({"message": f"Environment set to {env}"}), 200


@app.route("/warmup", methods=["GET"])
def warmup():
    try:
        from models import MonthlyProductData

        _ = MonthlyProductData.query.first()
        return jsonify({"message": "Server is ready"}), 200
    except Exception as e:
        return jsonify({"error": str(e), "tip": "Try calling /set_env first"}), 500


if __name__ == "__main__":
    app.run(debug=True)
