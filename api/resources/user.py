from extentions import db
from flask import request, g
from flask_restful import Resource
from datetime import datetime, timezone
from api.schemas.user import UserSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.helpers.user_helpers import get_user_id_from_token, get_user_by_user_id


class UserGet(Resource):
    method_decorators = [jwt_required()]

    def get(self):
        token = request.headers.get("Authorization")
        g.user = get_user_id_from_token(token)

        user_id = get_jwt_identity()
        users = get_user_by_user_id(user_id=user_id)

        schema = UserSchema()

        return {"result": schema.dump(users)}

    def delete(self):
        user_id = get_jwt_identity()
        users = get_user_by_user_id(user_id=user_id)

        users.is_deleted = True
        users.modified_at = datetime.now(timezone.utc)
        db.session.commit()

        return {"msg": "No Content"}, 204
