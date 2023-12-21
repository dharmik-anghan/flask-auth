import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

FLASK_RUN_PORT = os.environ.get("FLASK_RUN_PORT")
FLASK_RUN_HOST = os.environ.get("FLASK_RUN_HOST")
FLASK_DEBUG = os.environ.get("FLASK_DEBUG")
SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
FLASK_ENV = os.environ.get("FLASK_ENV")
FLASK_APP = os.environ.get("FLASK_APP")
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
JWT_TOKEN_LOCATION = ["headers"]
JWT_IDENTITY_CLAIM = "user_id"
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=120)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=15)