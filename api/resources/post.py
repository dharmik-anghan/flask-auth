from extentions import db
from models.post import Post
from flask_restful import Resource
from flask import request, jsonify, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.helpers.post_helpers import check_post_if_not_deleted
from api.schemas.post import PostResponseSchema, PostCreateSchema
from api.helpers.user_helpers import check_user_email_verification
from api.helpers.post_helpers import (
    update_post_count_in_user_table,
    update_post,
    delete_post,
    get_post_by_post_id,
    like_the_post,
    dislike_the_post,
)


class PostResource(Resource):
    method_decorators = [jwt_required()]

    @check_user_email_verification
    def get(self):
        post_id = request.args.get("post_id", type=int)
        user_id = get_jwt_identity()
        if post_id is not None:
            post = get_post_by_post_id(post_id=post_id)

            if post.user_id != user_id:
                abort(401)
            schema = PostResponseSchema()
            return {"posts": schema.dump(post)}

        posts = Post.query.filter_by(user_id=user_id, is_deleted=False).all()
        schema = PostResponseSchema(many=True)
        return {"posts": schema.dump(posts)}

    @check_user_email_verification
    def post(self):
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"})

        user_id = get_jwt_identity()
        data = request.get_json()
        data["user_id"] = user_id
        schema = PostCreateSchema()
        posts = schema.load(request.get_json())
        db.session.add(posts)
        db.session.commit()

        update_post_count_in_user_table(user_id)

        schema = PostResponseSchema()
        return {"msg": "Post Created", "post": schema.dump(posts)}

    @check_user_email_verification
    def put(self):
        post_id = request.args.get("post_id", type=int)
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"})

        user_id = get_jwt_identity()
        updated_post = update_post(
            post_id=post_id, data=request.get_json(), user_id=user_id
        )

        schema = PostResponseSchema()
        return {"msg": "Post updated successfully", "post": schema.dump(updated_post)}

    @check_user_email_verification
    def delete(self):
        post_id = request.args.get("post_id", type=int)
        user_id = get_jwt_identity()
        post_deleted = delete_post(post_id=post_id, user_id=user_id)

        if post_deleted:
            return {"msg": "Content no longer available"}, 204
        else:
            return {"msg": "Operation unsuccessfull"}, 200


class PostLikeResource(Resource):
    method_decorators = [jwt_required()]

    @check_user_email_verification
    @check_post_if_not_deleted
    def post(self):
        if request.path == "/posts/like":
            post_id = request.args.get("post_id")
            user_id = get_jwt_identity()

            if not post_id:
                return {"msg": "Missing post_id"}

            post_liked = like_the_post(user_id, post_id)

            if post_liked:
                return {"msg": "Post liked"}
            else:
                return {"msg": "Already liked by user"}
        else:
            return {"msg": "Path not found"}

    @check_post_if_not_deleted
    @check_user_email_verification
    def delete(self):
        if request.path == "/posts/dislike":
            post_id = request.args.get("post_id")
            user_id = get_jwt_identity()

            if not post_id:
                return {"msg": "Missing post_id"}

            post_disliked = dislike_the_post(user_id, post_id)

            if post_disliked:
                return {"msg": "Post disliked"}
            else:
                return {"msg": "Did't liked the post by user"}
        else:
            return {"msg": "Path not found"}
