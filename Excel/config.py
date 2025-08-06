import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_DEV_URI")


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DB_PROD_URI")
