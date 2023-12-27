from api.schemas.post_comment import PostCommentResponseSchema, PostCreateCommentSchema
from api.schemas.comment_and_reply_like import PostCommentLikeCreateSchema
from api.helpers.post_helpers import get_post_by_post_id
from models.post_comments import PostComment
from models.post_comment_likes import PostCommentLikes
from flask import abort
from extentions import db
from datetime import datetime, timezone
from models.post_comment_reply import PostCommentReply



def total_comment_on_post(post_id):
    comment_count = PostComment.query.filter_by(post_id=post_id).count()
    comment_reply_count = PostCommentReply.query.filter_by(post_id=post_id).count()
    return comment_count + comment_reply_count


def update_comment_count_post_table(post_id):
    try:
        comment_count = total_comment_on_post(post_id=post_id)
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
    try:
        comment = get_comment_by_user(comment_id, user_id=user_id)
        if comment.comment == data.get("comment"):
            return comment
        comment.comment = data.get("comment")
        comment.modified_at = datetime.now(timezone.utc)
        db.session.commit()

        return comment
    except Exception as e:
        abort(404, e)


def get_comment_by_comment_id(comment_id):
    comment = PostComment.query.filter_by(id=comment_id).first()
    if comment is None:
        abort(404, "No content found")
    return comment

def when_delete_comment_delete_all_data_related(comment_id):
    likes = PostCommentLikes.query.filter_by(comment_id=comment_id).all()
    for like in likes:
        db.session.delete(like)
    replies = PostCommentReply.query.filter_by(comment_id=comment_id).all()
    for reply in replies:
        db.session.delete(reply)

def delete_comment_on_post(comment_id, user_id, post_id):
    comment = get_comment_by_comment_id(comment_id)

    if comment.user_id == user_id:
        when_delete_comment_delete_all_data_related(comment_id)
        db.session.delete(comment)
        db.session.commit()
        update_comment_count_post_table(comment.post_id)
        return True
    else:
        post = get_post_by_post_id(post_id=post_id)
        if post.user_id == user_id:
            when_delete_comment_delete_all_data_related(comment_id)
            db.session.delete(comment)
            db.session.commit()
            update_comment_count_post_table(comment.post_id)
            return True

    return False


def comment_liked_by_user_or_not(user_id, comment_id, post_id):
    liked = PostCommentLikes.query.filter_by(
        user_id=user_id, comment_id=comment_id, post_id=post_id, reply_id=None
    ).first()
    if liked:
        return liked
    else:
        False


def update_comment_like_count(comment_id):
    comment = PostComment.query.filter_by(id=comment_id).first()
    comment.comment_like_count = PostCommentLikes.query.filter_by(
        comment_id=comment_id
    ).count()
    db.session.commit()


def like_the_comment(request, user_id):
    post_id = request.args.get("post_id")
    comment_id = request.args.get("comment_id")

    if comment_liked_by_user_or_not(user_id, comment_id, post_id):
        return False
    else:
        data = {}
        data["post_id"] = post_id
        data["comment_id"] = comment_id
        data["user_id"] = user_id

        schema = PostCommentLikeCreateSchema()

        liked = schema.load(data)

        db.session.add(liked)
        db.session.commit()

        update_comment_like_count(comment_id)

        return True


def dislike_the_comment(request, user_id):
    post_id = request.args.get("post_id")
    comment_id = request.args.get("comment_id")
    liked = comment_liked_by_user_or_not(user_id, comment_id, post_id)
    if liked:
        db.session.delete(liked)
        db.session.commit()
        update_comment_like_count(comment_id)

        return True
    else:
        return False
