from models.post import Post
from models.post_likes import PostLike
from api.helpers.user_helpers import get_user_by_user_id
from api.schemas.post_like import PostLikeCreateSchema
from flask import abort, jsonify
from extentions import db
from datetime import datetime, timezone

def update_post_count_in_user_table(user_id):
    user = get_user_by_user_id(user_id)
    post_count = Post.query.filter_by(
        user_id=user_id, is_deleted=False
    ).count()

    user.post_count = post_count
    db.session.commit()

    return True

def get_post_by_post_id(post_id):
    post = Post.query.filter_by(id=post_id, is_deleted=False).first()
    return abort(404, "Post not found") if post is None else post

def update_post(user_id, post_id, data):
    post = get_post_by_post_id(post_id)

    if post.user_id != user_id:
        abort(401)

    post.caption = data.get("caption")
    post.modified_at = datetime.now(timezone.utc)
    db.session.commit()

    post = get_post_by_post_id(post_id)

    return post

def delete_post(user_id, post_id):
    post = get_post_by_post_id(post_id)

    if post.user_id != user_id:
        abort(401)

    try:
        post.is_deleted = True
        post.modified_at = datetime.now(timezone.utc)
        db.session.commit()
        update_post_count_in_user_table(user_id)
        return True
    except Exception as e:
        return e
    
def update_like_count_post_table(post_id):
    try:
        like_count = PostLike.query.filter_by(post_id=post_id).count()
        post = get_post_by_post_id(post_id)
        post.like_count = like_count
        db.session.commit()
    except Exception as e:
        abort(404, f"{e}")

def like_the_post(user_id, post_id):
    post_liked_by = PostLike.query.filter_by(liked_by=user_id, post_id=post_id).first() 
    if post_liked_by is None:
        schema = PostLikeCreateSchema()
        post_liked = schema.load({"post_id": post_id, "liked_by": user_id})
        db.session.add(post_liked)
        db.session.commit()
        update_like_count_post_table(post_id)

        return True
    else:
        return False
    
def dislike_the_post(user_id, post_id):
    post_liked_by = PostLike.query.filter_by(liked_by=user_id, post_id=post_id).first()
    post = get_post_by_post_id(post_id=post_id)
    if post_liked_by is not None:
        db.session.delete(post_liked_by)
        db.session.commit()
        update_like_count_post_table(post_id)

        return True
    else:
        return False