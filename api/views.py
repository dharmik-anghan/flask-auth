from flask import Blueprint
from flask_restful import Api

from api.resources.user import UserGet
from api.resources.sentotp import SentOTP
from api.resources.verify_account import VerifyAccount
from api.resources.reset_password import ResetPassword
from api.resources.forgot_password import ForgotPassword

user_blueprint = Blueprint("user", __name__, url_prefix="/user")
user_api = Api(user_blueprint, errors=user_blueprint.errorhandler)
user_api.add_resource(UserGet, "/")


otp_blueprint = Blueprint("otp", __name__, url_prefix="/otp")
otp_api = Api(otp_blueprint, errors=otp_blueprint.errorhandler)
otp_api.add_resource(SentOTP, "/send-otp")


verify_ac_blueprint = Blueprint("verify_ac", __name__, url_prefix="/verify-account")
verify_ac_api = Api(verify_ac_blueprint, errors=verify_ac_blueprint.errorhandler)
verify_ac_api.add_resource(VerifyAccount, "/")


reset_password_blueprint = Blueprint("reset_ac", __name__, url_prefix="/reset-password")
reset_password_api = Api(
    reset_password_blueprint, errors=reset_password_blueprint.errorhandler
)
reset_password_api.add_resource(ResetPassword, "/")


forgot_password_blueprint = Blueprint(
    "forgot_password", __name__, url_prefix="/forgot-password"
)
forgot_password_api = Api(
    forgot_password_blueprint, errors=forgot_password_blueprint.errorhandler
)
forgot_password_api.add_resource(ForgotPassword, "/")
