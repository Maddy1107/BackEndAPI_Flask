from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

from config_state import ConfigState

# Load variables from .env
load_dotenv()

db = SQLAlchemy()
migrate = Migrate()


def init_db(app):
    if ConfigState.current_env == "production":
        db_uri = os.getenv("DB_PROD_URI")
    else:
        db_uri = os.getenv("DB_DEV_URI")

    if not db_uri:
        raise RuntimeError("❌ Environment variable NEON_DB_URI is not set.")

    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)
