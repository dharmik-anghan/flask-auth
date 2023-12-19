from flask_restful import Resource
from flask_jwt_extended import jwt_required
from api.resources.helpers import get_user_id_from_token, get_user_by_user_id
from flask import request, jsonify
from extentions import db, pwd_context
from datetime import datetime, timezone


class ResetPassword(Resource):
    method_decorators = [jwt_required()]

    def post(self):
        user_id = get_user_id_from_token(request.headers)
        users = get_user_by_user_id(user_id=user_id)
        old_password = request.json["old_password"]
        new_password = request.json["new_password"]

        if pwd_context.verify(old_password, users._password):
            users.password = new_password
            users.modified_at = datetime.now(timezone.utc)
            db.session.commit()
        else:
            return jsonify({"msg": "Incorrect password"})

        return jsonify({"msg": "Reset-password Successfully"})
