from flask_sqlalchemy import SQLAlchemy
from passlib.context import CryptContext
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from email.message import EmailMessage
from authlib.integrations.flask_client import OAuth

db = SQLAlchemy()
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
jwt = JWTManager()
ma = Marshmallow()
msg = EmailMessage()
oauth = OAuth()
