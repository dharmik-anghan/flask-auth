from extentions import db
from datetime import datetime

class RequestToUser(db.Model):
    __tablename__ = "request_to_user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), index=True, nullable=False)
    requested_by = db.Column(db.Integer, db.ForeignKey("users.id"), index=True, nullable=False)
    request_accepted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now)

    user_request_to_table = db.relationship("User", back_populates="user_request_to", foreign_keys=[user_id])
    user_request_by_table = db.relationship("User", back_populates="user_request_by", foreign_keys=[requested_by])