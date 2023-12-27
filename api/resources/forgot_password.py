from flask_restful import Resource
from api.helpers.user_helpers import forgot_database_user_password, get_user_by_mail, get_latest_otp
from flask import request, jsonify
from extentions import db

class ForgotPassword(Resource):
    def post(self):
        email = request.json["email"]
        otp = request.json["otp"]
        password = request.json["password"]

        success_forgot = forgot_database_user_password(db=db, email=email, otp=otp, new_password=password)

        if success_forgot is False:
            return jsonify({"msg": "Somthing went-wrong"})
        

        return jsonify({"msg": "Successfully changed your password"})
