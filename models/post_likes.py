from extentions import db
from datetime import datetime

class PostLike(db.Model):
    __tablename__ = "post_likes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    liked_by = db.Column(db.Integer, db. ForeignKey("users.id"), nullable=False)
    liked_at = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.now)

    post_table = db.relationship("Post", back_populates="post_like_table")
    user_table = db.relationship("User", back_populates="post_like_table")