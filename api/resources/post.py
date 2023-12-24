from flask_restful import Resource
from api.schemas.post import PostResponseSchema, PostSchema, PostCreateSchema
from flask import request, jsonify
from extentions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User

class PostResource(Resource):
    method_decorators = [jwt_required()]

    def get(self):
        pass

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

        schema = PostResponseSchema()
        return {"msg":"Post Created", "post": schema.dump(posts)}

    def put(self):
        pass

    def delete(self):
        pass