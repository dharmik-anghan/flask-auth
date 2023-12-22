from extentions import db
from datetime import datetime


class PostCommentLikes(db.Model):
    __tablename__ = "comment_likes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment_id = db.Column(
        db.Integer, db.ForeignKey("post_comments.id"), nullable=False, index=True
    )
    reply_id = db.Column(
        db.Integer, db.ForeignKey("post_comments_reply.id"), nullable=True, index=True
    )
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True), nullable=False, default=datetime.now
    )

    # post.py
    post_table = db.relationship("Post", back_populates="post_comment_likes_table")

    # user.py
    user_table = db.relationship("User", back_populates="post_comment_likes_table")

    # comment.py
    post_comment_table = db.relationship(
        "PostComment", back_populates="post_comment_likes_table"
    )

    post_comment_reply_table= db.relationship(
        "PostCommentReply", back_populates="post_comment_likes_table"
    )
