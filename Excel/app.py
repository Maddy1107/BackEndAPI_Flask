from flask import Flask, jsonify, request
from config_state import ConfigState
from database import preload_db, reconfigure_db, db

# ✅ Create and preload the app + DB with dummy connection
app = Flask(__name__)
preload_db(app)  # This makes sure `db.Model` is always bound


# Register routes early
@app.route("/set_env", methods=["POST"])
def set_env():
    data = request.get_json()
    env = data.get("build_type", "development").lower()

    if env not in ["development", "production"]:
        return jsonify({"error": "Invalid env"}), 400

    ConfigState.current_env = env
    ConfigState.db_initialized = True

    try:
        reconfigure_db(app)
        return jsonify({"message": f"Env set to {env}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/warmup", methods=["GET"])
def warmup():
    if not ConfigState.db_initialized:
        return jsonify({"error": "Env not set. Call /set_env first."}), 500

    try:
        from models import MonthlyProductData

        item = MonthlyProductData.query.first()
        return jsonify({"ok": True, "product": item.to_dict() if item else None}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
