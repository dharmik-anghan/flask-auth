from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.helpers.post_helpers import check_post_if_not_deleted
from api.schemas.post_comment import PostCommentResponseSchema
from api.helpers.user_helpers import check_user_email_verification
from api.helpers.post_comment_helpers import (
    comment_on_post,
    get_comments_on_post,
    update_comment_on_post,
    delete_comment_on_post,
    like_the_comment,
    dislike_the_comment,
)


class PostCommentResource(Resource):
    method_decorators = [jwt_required()]

    @check_user_email_verification
    @check_post_if_not_deleted
    def get(self):
        if request.path == "/posts/viewcomments":
            post_id = request.args.get("post_id", type=int)

            if post_id is None:
                return {"msg": "Missing post id"}

            comments = get_comments_on_post(post_id)

            schema = PostCommentResponseSchema(many=True)

            return {"comments": schema.dump(comments)}
        else:
            return {"msg": "Path not defined"}, 405

    @check_user_email_verification
    @check_post_if_not_deleted
    def post(self):
        post_id = request.args.get("post_id", type=int)

        if post_id is None:
            return {"msg": "Missing post id"}
        if not request.is_json:
            return {"msg": "Missing json in request body"}

        user_id = get_jwt_identity()
        data = request.get_json()
        data["post_id"] = post_id
        data["user_id"] = user_id

        comment = comment_on_post(data)
        return {"msg": "Comment Created", "Comment": comment}

    @check_user_email_verification
    @check_post_if_not_deleted
    def put(self):
        if request.path == "/posts/update-comment":
            comment_id = request.args.get("comment_id", type=int)

            if comment_id is None:
                return {"msg": "Missing comment id"}
            if not request.is_json:
                return {"msg": "Missing json in request body"}

            user_id = get_jwt_identity()

            updated_comment = update_comment_on_post(
                comment_id, user_id, request.get_json()
            )

            schema = PostCommentResponseSchema()

            return {"msg": "Comment Updated", "Commment": schema.dump(updated_comment)}
        else:
            return {"msg": "Path not defined"}, 405

    @check_user_email_verification
    @check_post_if_not_deleted
    def delete(self):
        if request.path == "/posts/delete-comment":
            comment_id = request.args.get("comment_id", type=int)

            if comment_id is None:
                return {"msg": "Missing comment id"}

            user_id = get_jwt_identity()
            post_id = request.args.get("post_id")

            deleted_comment = delete_comment_on_post(comment_id, user_id, post_id)

            if deleted_comment:
                return {"msg": "Comment deleted"}, 204
            else:
                return {"msg": "Operation unsuccesfull"}
        else:
            return {"msg": "Path not defined"}, 405


class CommentLike(Resource):
    method_decorators = [jwt_required()]

    def post(self):
        if request.path == "/posts/like-comment":
            comment_id = request.args.get("comment_id")
            post_id = request.args.get("post_id")
            user_id = get_jwt_identity()

            if comment_id and post_id:
                liked_comment = like_the_comment(request, user_id)

                if liked_comment:
                    return {"msg": "Liked comment"}
                else:
                    return {"msg": "Alredy Liked"}

    def delete(self):
        if request.path == "/posts/like-comment":
            comment_id = request.args.get("comment_id")
            post_id = request.args.get("post_id")
            user_id = get_jwt_identity()

            if comment_id and post_id:
                disliked_comment = dislike_the_comment(request, user_id)

                if disliked_comment:
                    return {"msg": "disiked comment"}
                else:
                    return {"msg": "No liked comment"}, 404
