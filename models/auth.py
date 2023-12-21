from extentions import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID


class TokenBlockList(db.Model):
    __tablename__ = "token_block_list"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    jti = db.Column(db.String, nullable=False)
    token_type = db.Column(db.String, nullable=False)
    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False, index=True
    )
    revoked_at = db.Column(db.DateTime(timezone=True))
    expires = db.Column(
        db.DateTime(timezone=True), nullable=False, default=datetime.now
    )

    user = db.relationship("User", back_populates="token")
