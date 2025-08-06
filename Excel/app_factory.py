from flask import Flask
from config import DevelopmentConfig, ProductionConfig
from database import db, migrate
from models import MonthlyProductData, ProductRequest


def create_app(env="development"):
    app = Flask(__name__)

    if env == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()

    return app
