from extentions import db, pwd_context

from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from models.otp import OTPDatabase
from models.auth import TokenBlockList
from models.post import Post
from models.post_comments import PostComment
from models.post_comment_likes import PostCommentLikes
from models.follower_following import FollowerFollowing
from models.post_comment_reply import PostCommentReply
from models.user_request import RequestToUser


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    full_name = db.Column(db.String(40), nullable=False)
    username = db.Column(db.String(15), unique=True, nullable=False)
    _password = db.Column("password", db.String(255), nullable=False)
    follower_count = db.Column(db.Integer, default=0)
    following_count = db.Column(db.Integer, default=0)
    post_count = db.Column(db.Integer, default=0)

    is_public = db.Column(db.Boolean, nullable=False)
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

    # post.py
    post_table = db.relationship("Post", back_populates="user_table")

    # post_likes.py
    post_like_table = db.relationship("PostLike", back_populates="user_table")

    # post_comment.py
    post_comment_table = db.relationship("PostComment", back_populates="user_table")

    # post_comment_likes.py
    post_comment_likes_table = db.relationship(
        "PostCommentLikes", back_populates="user_table"
    )

    # follower_following.py
    follower = db.relationship(
        "FollowerFollowing",
        back_populates="user_follower_table",
        foreign_keys="FollowerFollowing.followed_by",
    )
    following = db.relationship(
        "FollowerFollowing",
        back_populates="user_following_table",
        foreign_keys="FollowerFollowing.user_id",
    )

    post_comment_reply_table = db.relationship(
        "PostCommentReply", back_populates="user_table"
    )

    user_request_to = db.relationship(
        "RequestToUser",
        back_populates="user_request_to_table",
        foreign_keys="RequestToUser.user_id"
    )
    user_request_by = db.relationship(
        "RequestToUser",
        back_populates="user_request_by_table",
        foreign_keys="RequestToUser.requested_by",
    )
