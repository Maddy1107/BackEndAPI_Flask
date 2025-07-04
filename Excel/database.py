from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def init_db(app):
    uri = "postgresql://neondb_owner:npg_16dtTzOgnhfU@ep-broad-shape-a897iy1b-pooler.eastus2.azure.neon.tech/neondb?sslmode=require&channel_binding=require"

    app.config["SQLALCHEMY_DATABASE_URI"] = uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate.init_app(app, db)  # ✅ Now you're using Flask-Migrate
