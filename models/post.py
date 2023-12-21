from extentions import db
from datetime import datetime
from models.post_likes import PostLike


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post = db.Column(db.String, nullable=False)
    caption = db.Column(db.String, nullable=True)
    created_at = db.Column(
        db.DateTime(timezone=True), nullable=False, default=datetime.now
    )
    modified_at = db.Column(db.DateTime(timezone=True), default=datetime.now)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    like_count = db.Column(db.Integer, nullable=True)
    comment_count = db.Column(db.Integer, nullable=True)

    user_table = db.relationship("User", back_populates="post_table")
    post_like_table = db.relationship("PostLike", back_populates="post_table")
