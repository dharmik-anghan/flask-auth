from extentions import db, pwd_context

from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    full_name = db.Column(db.String(40), nullable=False)
    username = db.Column(db.String(15), unique=True, nullable=False)
    _password = db.Column("password", db.String(255), nullable=False)

    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    is_social = db.Column(db.Boolean, default=False, nullable=False)

    created_at = db.Column(
        db.DateTime(timezone=True), nullable=False, default=datetime.now
    )
    modified_at = db.Column(db.DateTime(timezone=True))

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = pwd_context.hash(value)

    token = db.relationship("TokenBlockList", back_populates="user")
    user_otp = db.relationship("OTPDatabase", back_populates="user_table")


class OTPDatabase(db.Model):
    __tablename__ = "otpdatabase"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    _otp = db.Column("otp", db.String, nullable=False)
    otp_received_at = db.Column(
        db.DateTime(timezone=True), nullable=False, default=datetime.now
    )
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user_table = db.relationship("User", back_populates="user_otp")
