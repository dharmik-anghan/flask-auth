from flask import abort
from extentions import db
from datetime import datetime, timezone
from models.post_comment_reply import PostCommentReply
from models.post_comment_likes import PostCommentLikes
from api.helpers.post_comment_helpers import get_comment_by_comment_id
from api.schemas.comment_and_reply_like import PostReplyLikeCreateSchema
from api.helpers.post_comment_helpers import update_comment_count_post_table
from api.schemas.post_comment_reply import (
    PostCommentReplyResponseSchema,
    PostCreateCommentSchema,
)


def get_comments_reply_on_post(comment_id):
    reply = PostCommentReply.query.filter_by(comment_id=comment_id).all()
    if reply is None:
        abort(404, "No content found")
    return reply


def update_reply_count_comment_table(comment_id):
    try:
        comment_count = PostCommentReply.query.filter_by(comment_id=comment_id).count()
        comment = get_comment_by_comment_id(comment_id=comment_id)
        comment.comment_reply_count = comment_count
        db.session.commit()
    except Exception as e:
        abort(404, e)


def reply_on_post(data):
    try:
        schema = PostCreateCommentSchema()
        comment = schema.load(data)
        db.session.add(comment)
        db.session.commit()
        update_comment_count_post_table(data["post_id"])
        update_reply_count_comment_table(data["comment_id"])
        schema = PostCommentReplyResponseSchema()
        return schema.dump(comment)
    except Exception as e:
        abort(404, e)


def get_reply_by_user(reply_id, user_id, comment_id):
    reply = PostCommentReply.query.filter_by(
        id=reply_id, user_id=user_id, comment_id=comment_id
    ).first()
    if not reply:
        abort(404, "No reply found")

    return reply


def update_reply_on_comment(reply_id, comment_id, user_id, data):
    try:
        reply = get_reply_by_user(reply_id, user_id=user_id, comment_id=comment_id)
        if reply.comment_reply == data.get("comment_reply"):
            return reply
        reply.comment_reply = data.get("comment_reply")
        reply.modified_at = datetime.now(timezone.utc)
        db.session.commit()

        return reply
    except Exception as e:
        abort(404, e)


def reply_liked_by_user_or_not(user_id, comment_id, post_id, reply_id):
    liked = PostCommentLikes.query.filter_by(
        user_id=user_id, comment_id=comment_id, reply_id=reply_id, post_id=post_id
    ).first()
    if liked:
        return liked
    else:
        False


def delete_reply_in_comment(reply_id, comment_id, user_id, post_id):
    try:
        reply = get_reply_by_user(reply_id, user_id=user_id, comment_id=comment_id)
        reply_liked = reply_liked_by_user_or_not(user_id, comment_id, post_id, reply_id)
        db.session.delete(reply_liked)
        db.session.delete(reply)
        db.session.commit()
        update_comment_count_post_table(post_id)
        update_reply_count_comment_table(comment_id)
        return True
    except Exception as e:
        abort(404, e)


def update_reply_like_count(reply_id):
    reply = PostCommentReply.query.filter_by(id=reply_id).first()
    reply.reply_like_count = PostCommentLikes.query.filter_by(reply_id=reply_id).count()
    db.session.commit()


def like_the_reply(request, user_id):
    post_id = request.args.get("post_id")
    comment_id = request.args.get("comment_id")
    reply_id = request.args.get("reply_id")

    if reply_liked_by_user_or_not(user_id, comment_id, post_id, reply_id):
        return False
    else:
        data = {}
        data["post_id"] = post_id
        data["comment_id"] = comment_id
        data["user_id"] = user_id
        data["reply_id"] = reply_id

        schema = PostReplyLikeCreateSchema()

        liked = schema.load(data)

        db.session.add(liked)
        db.session.commit()

        update_reply_like_count(reply_id)

        return True


def dislike_the_reply(request, user_id):
    try:
        post_id = request.args.get("post_id")
        comment_id = request.args.get("comment_id")
        reply_id = request.args["reply_id"]
        liked = reply_liked_by_user_or_not(user_id, comment_id, post_id, reply_id)
        if liked:
            db.session.delete(liked)
            db.session.commit()
            update_reply_like_count(reply_id)

            return True
        else:
            return False
    except Exception as e:
        abort(500, e)
