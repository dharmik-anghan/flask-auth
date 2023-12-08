from flask_restful import Resource
from flask import request, jsonify
from models.user import User, OTPDatabase
from extentions import db
from api.resources.helpers import get_latest_otp, verify_user_account


class VerifyAccount(Resource):
    def post(self):
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"})

        email = request.json.get("email")
        otp = request.json.get("otp")

        if email is None or otp is None:
            return jsonify({"msg": "Enter correct email or OTP"})

        account_verifies = verify_user_account(db=db, email=email, otp=otp)

        if account_verifies:
            return jsonify({"msg": "User Verified"})
        else:
            return jsonify({"msg": "Enter correct OTP."})
