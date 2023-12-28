from extentions import db
from datetime import datetime

class RequestToUser(db.Model):
    __tablename__ = "request_to_user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    requested_to = db.Column(db.Integer, db.ForeignKey("users.id"), index=True, nullable=False)
    requested_by = db.Column(db.Integer, db.ForeignKey("users.id"), index=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.now)
    user_request_to_table = db.relationship("User", back_populates="user_request_to", foreign_keys=[requested_to])
    user_request_by_table = db.relationship("User", back_populates="user_request_by", foreign_keys=[requested_by])