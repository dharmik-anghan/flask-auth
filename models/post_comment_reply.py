from extentions import db
from datetime import datetime
from models.post_comment_likes import PostCommentLikes

class PostCommentReply(db.Model):
    __tablename__ = "post_comments_reply"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment_reply = db.Column(db.String, nullable=False)
    comment_id = db.Column(
        db.Integer, db.ForeignKey("post_comments.id"), nullable=False, index=True
    )
    post_id = db.Column(
        db.Integer, db.ForeignKey("posts.id"), nullable=False, index=True
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    created_at = db.Column(
        db.DateTime(timezone=True), nullable=False, default=datetime.now
    )
    modified_at = db.Column(db.DateTime(timezone=True))
    reply_like_count = db.Column(db.Integer, default=0)

    # post.py
    post_table = db.relationship("Post", back_populates="post_comment_reply_table")

    # user.py
    user_table = db.relationship("User", back_populates="post_comment_reply_table")

    # post_comment_likes.py
    post_comment_likes_table = db.relationship(
        "PostCommentLikes", back_populates="post_comment_reply_table"
    )

    post_comment_table = db.relationship("PostComment", back_populates="post_comment_reply_table")

