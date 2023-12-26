from api.schemas.post_comment import PostCommentResponseSchema, PostCreateCommentSchema
from api.helpers.post_helpers import get_post_by_post_id
from models.post_comments import PostComment
from flask import abort
from extentions import db
from datetime import datetime, timezone

def update_comment_count_post_table(post_id):
    try:
        comment_count = PostComment.query.filter_by(post_id=post_id).count()
        post = get_post_by_post_id(post_id)
        post.comment_count = comment_count
        db.session.commit()
    except Exception as e:
        abort(404, f"{e}")

def get_comment_by_user(comment_id, user_id):
    comment = PostComment.query.filter_by(id=comment_id, user_id=user_id).first()
    if comment is None:
        abort(401)
    return comment

def comment_on_post(data):
    schema = PostCreateCommentSchema()
    comment = schema.load(data)
    db.session.add(comment)
    db.session.commit()
    update_comment_count_post_table(data["post_id"])
    schema = PostCommentResponseSchema()
    return schema.dump(comment)

def get_comments_on_post(post_id):
    return PostComment.query.filter_by(post_id=post_id).all()

def update_comment_on_post(comment_id, user_id, data):
    comment = get_comment_by_user(comment_id, user_id=user_id)
    comment.comment = data.get("comment")
    comment.modified_at = datetime.now(timezone.utc)
    db.session.commit()

    return comment

def get_comment_by_comment_id(comment_id):
    comment = PostComment.query.filter_by(id=comment_id).first()
    if comment is None:
        abort(404, "No content found")
    return comment

def delete_comment_on_post(comment_id, user_id, post_id):
    comment = get_comment_by_comment_id(comment_id)

    if comment.user_id == user_id:
        db.session.delete(comment)
        db.session.commit()
        update_comment_count_post_table(comment.post_id)
        return True
    else:
        post = get_post_by_post_id(post_id=post_id)
        if post.user_id == user_id:
            db.session.delete(comment)
            db.session.commit()
            update_comment_count_post_table(comment.post_id)
            return True
        
    return False


    
