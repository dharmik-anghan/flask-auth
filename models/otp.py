from extentions import db, pwd_context

from datetime import datetime

class OTPDatabase(db.Model):
    __tablename__ = "otpdatabase"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    _otp = db.Column("otp", db.String, nullable=False)
    otp_received_at = db.Column(
        db.DateTime(timezone=True), nullable=False, default=datetime.now
    )
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user_table = db.relationship("User", back_populates="user_otp")