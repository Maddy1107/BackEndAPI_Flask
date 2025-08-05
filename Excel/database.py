from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config_state import ConfigState
import os

db = SQLAlchemy()
migrate = Migrate()


def preload_db(app):  # Called at startup with dummy URI
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate.init_app(app, db)


def reconfigure_db(app):

    if "SQLALCHEMY_DATABASE_URI" in app.config:
        return

    # Called when Unity hits /set_env
    env = ConfigState.current_env or "development"
    uri = os.getenv("DB_PROD_URI") if env == "production" else os.getenv("DB_DEV_URI")

    if not uri:
        raise RuntimeError("Missing DB URI")

    print(f"[INFO] Switching DB to: {env} → {uri}")
    app.config["SQLALCHEMY_DATABASE_URI"] = uri
    db.engine.dispose()  # kill old connection pool
    ConfigState.db_initialized = True
