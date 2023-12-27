from extentions import db
from datetime import datetime
from models.post_likes import PostLike
from models.post_comments import PostComment
from models.post_comment_likes import PostCommentLikes
from models.post_comment_reply import PostCommentReply


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post = db.Column(db.String, nullable=False)
    caption = db.Column(db.String, nullable=True)
    created_at = db.Column(
        db.DateTime(timezone=True), nullable=False, default=datetime.now
    )
    modified_at = db.Column(db.DateTime(timezone=True))
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    like_count = db.Column(db.Integer, default=0)
    comment_count = db.Column(db.Integer, default=0)
    is_deleted = db.Column(db.Boolean, default=False)

    user_table = db.relationship("User", back_populates="post_table")
    post_like_table = db.relationship("PostLike", back_populates="post_table")

    post_comment_table = db.relationship("PostComment", back_populates="post_table")

    post_comment_reply_table = db.relationship("PostCommentReply", back_populates="post_table")
    # post_comment_likes.py
    post_comment_likes_table = db.relationship(
        "PostCommentLikes", back_populates="post_table"
    )

