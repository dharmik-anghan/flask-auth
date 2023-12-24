from flask_restful import Resource
from flask import request, jsonify
from utils.sent_mail_to_user import sent_otp
from extentions import db, pwd_context
from api.schemas.otp_schema import OTPSchema
from api.resources.helpers import get_user_by_mail, get_otp_details
from datetime import datetime, timezone


class SentOTP(Resource):
    def post(self):
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"})

        email = request.json["email"]

        user = get_user_by_mail(email=email)
        user_id = user.id
        user_email = user.email

        if user is None:
            return {"msg": "Register your self!!!"}, 404

        otp = sent_otp(mail_to=user_email)
        hashed_otp = pwd_context.hash(otp)

        otp_from_db = get_otp_details(user_id=user_id)

        if otp_from_db:
            otp_from_db._otp = hashed_otp
            otp_from_db.otp_received_at = datetime.now(timezone.utc)
        else:
            schema = OTPSchema()

            store_otp = schema.load(data={"user_id": user_id, "_otp": hashed_otp})
            db.session.add(store_otp)

        db.session.commit()

        return jsonify({"msg": "OTP sent successfully."})
