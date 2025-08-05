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
    env = os.getenv("APP_ENV", "development").lower()
    if ConfigState.current_env == "production":
        db_uri = os.getenv("DB_PROD_URI")
    else:
        db_uri = os.getenv("DB_DEV_URI")

    print(f"Using {env} database URI: {db_uri}")
    print(f"Initializing database for {env} environment...")
    if not db_uri:
        raise RuntimeError("❌ Environment variable NEON_DB_URI is not set.")

    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["DEBUG"] = env != "production"

    db.init_app(app)
    migrate.init_app(app, db)

    print(f"DB connected [{env}]")
