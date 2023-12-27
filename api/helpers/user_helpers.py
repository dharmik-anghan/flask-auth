import os
from flask import abort
from models.user import User
from dotenv import load_dotenv
from models.user import OTPDatabase
from extentions import pwd_context
from flask_jwt_extended import decode_token
from flask_jwt_extended import get_jwt_identity
from datetime import datetime, timedelta, timezone

load_dotenv()


def get_user_by_mail(email):
    user = User.query.filter_by(email=email, is_deleted=False).first()

    if user is None:
        abort(404, "User not found")

    return user


def get_user_by_user_id(user_id):
    user = User.query.filter_by(
        id=user_id, is_deleted=False, is_active=True
    ).first()

    if user is None:
        abort(404, "User not found")

    return user


def get_diff_btw_time(registered_time: datetime):
    current_time = datetime.now(timezone.utc)
    diff_btw_time = current_time - registered_time
    return diff_btw_time

def get_otp_details(user_id):
    return (
        OTPDatabase.query.filter_by(user_id=user_id)
        .order_by(OTPDatabase.otp_received_at.desc())
        .first()
    )

def get_latest_otp(user_id: int):
    latest_otp = get_otp_details(user_id)

    if latest_otp is None:
        return False

    otp_expires_in = int(os.environ.get("OTP_EXPIRES_IN"))

    diff_btw_time = get_diff_btw_time(latest_otp.otp_received_at)
    condition = diff_btw_time > timedelta(minutes=otp_expires_in)
    if condition:
        return abort(410, "OTP has expired")

    return latest_otp


def verify_user_account(db, email, otp):
    user = get_user_by_mail(email=email)

    user_id = user.id

    if user.is_verified == True:
        abort(409, "User already verified")

    latest_otp = get_latest_otp(user_id=user_id)

    try:
        if pwd_context.verify(otp, latest_otp._otp):
            user.is_verified = True
            db.session.commit()
            return True
        else:
            return False
    except Exception as e:
        return e


def get_user_id_from_token(token):
    token = token.split(" ")
    decoded_token = decode_token(token[1])

    return decoded_token


def forgot_database_user_password(db, email, otp, new_password):
    user = get_user_by_mail(email=email)

    user_id = user.id

    latest_otp = get_latest_otp(user_id=user_id)

    if otp == latest_otp._otp:
        user.password = new_password
        user.modified_at = datetime.now(timezone.utc)
        db.session.commit()
        return True
    else:
        return False
    

def check_user_email_verification(func):
    def wrapper(self, *args, **kwargs):
        user_id = get_jwt_identity()
        user = get_user_by_user_id(user_id) 
        if user.is_verified is False:
            abort(401, "Account not verified")
        return func(self, *args, **kwargs)
        
    return wrapper