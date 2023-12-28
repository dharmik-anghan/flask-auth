from extentions import db
from datetime import datetime

class FollowerFollowing(db.Model):
    __tablename__ = "followers_followings"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    followed_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    followed_to = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    followed_at = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.now)

    user_following_table = db.relationship("User", back_populates="following", foreign_keys=[followed_to])
    user_follower_table = db.relationship("User", back_populates="follower", foreign_keys=[followed_by])
    