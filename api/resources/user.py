from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource

from api.schemas.user import UserSchema

from api.resources.helpers import get_user_id_from_token, get_user_by_user_id


class UserGet(Resource):
    method_decorators = [jwt_required()]

    def get(self):
        user_id = get_user_id_from_token(request.headers)
        users = get_user_by_user_id(user_id=user_id)

        schema = UserSchema()

        return {"result": schema.dump(users)}
