from flask_restful import Resource
from api.helpers.user_helpers import check_user_email_verification
from api.helpers.post_comment_reply_helpers import (
    reply_on_post,
    get_comments_reply_on_post,
    update_reply_on_comment,
    delete_reply_in_comment,
    like_the_reply,
    dislike_the_reply,
)
from api.helpers.post_helpers import check_post_if_not_deleted
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from api.schemas.post_comment_reply import PostCreateCommentSchema,PostCommentReplyResponseSchema


class PostCommentReplyResource(Resource):
    method_decorators = [jwt_required()]

    @check_user_email_verification
    @check_post_if_not_deleted
    def get(self):
        if request.path == "/posts/comment/viewreplies":
            post_id = request.args.get("post_id", type=int)
            comment_id = request.args.get("comment_id")

            if post_id is None and comment_id is None:
                return {"msg": "Missing post or comment id"}

            replies = get_comments_reply_on_post(comment_id)

            schema = PostCommentReplyResponseSchema(many=True)

            return {"replies": schema.dump(replies)}
        else:
            return {"msg": "Path not defined"}, 405

    @check_user_email_verification
    @check_post_if_not_deleted
    def post(self):
        post_id = request.args.get("post_id", type=int)
        comment_id = request.args.get("comment_id", type=int)

        if post_id is None and comment_id is None:
            return {"msg": "Missing post or comment id"}
        if not request.is_json:
            return {"msg": "Missing json in request body"}

        user_id = get_jwt_identity()
        data = request.get_json()
        data["post_id"] = post_id
        data["user_id"] = user_id
        data["comment_id"] = comment_id

        comment = reply_on_post(data)
        return {"msg": "Reply Created", "Comment": comment}

    @check_user_email_verification
    @check_post_if_not_deleted
    def put(self):
        if request.path == "/posts/comment/update-reply":
            comment_id = request.args.get("comment_id", type=int)
            reply_id = request.args.get("reply_id", type=int)

            if comment_id is None:
                return {"msg": "Missing comment id"}
            if not request.is_json:
                return {"msg": "Missing json in request body"}

            user_id = get_jwt_identity()

            updated_comment = update_reply_on_comment(
                reply_id, comment_id, user_id, request.get_json()
            )

            schema = PostCreateCommentSchema()

            return {"msg": "Comment Updated", "Commment": schema.dump(updated_comment)}
        else:
            return {"msg": "Path not defined"}, 405

    @check_user_email_verification
    @check_post_if_not_deleted
    def delete(self):
        if request.path == "/posts/comment/delete-reply":
            comment_id = request.args.get("comment_id", type=int)
            reply_id = request.args.get("reply_id", type=int)

            if comment_id is None:
                return {"msg": "Missing comment id"}

            user_id = get_jwt_identity()
            post_id = request.args.get("post_id")

            deleted_comment = delete_reply_in_comment(reply_id, comment_id, user_id, post_id)

            if deleted_comment:
                return {"msg": "Comment deleted"}, 204
            else:
                return {"msg": "Operation unsuccesfull"}
        else:
            return {"msg": "Path not defined"}, 405
        

class   ReplyLike(Resource):
    method_decorators = [jwt_required()]

    def post(self):
        if request.path == "/posts/like-reply":
            comment_id = request.args.get("comment_id")
            post_id = request.args.get("post_id")
            reply_id = request.args.get("reply_id")
            user_id = get_jwt_identity()

            if comment_id and post_id and reply_id:
                liked_comment = like_the_reply(request, user_id)

                if liked_comment:
                    return {"msg": "Liked Reply"}
                else:
                    return {"msg": "Alredy Liked"}
            else:
                return {"msg": "Params missing"}
        else:
            return {"msg": "Path not defined"}, 405        

    def delete(self):
        if request.path == "/posts/dislike-reply":
            comment_id = request.args.get("comment_id")
            post_id = request.args.get("post_id")
            reply_id = request.args.get("reply_id")

            user_id = get_jwt_identity()

            if comment_id and post_id and reply_id:
                disliked_comment = dislike_the_reply(request, user_id)

                if disliked_comment:
                    return {"msg": "disiked reply"}
                else:
                    return {"msg": "No liked reply"}, 404
            else:
                return {"msg": "Params missing"}
        else:
            return {"msg": "Path not defined"}, 405
            