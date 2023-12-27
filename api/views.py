from flask import Blueprint
from flask_restful import Api

from api.resources.user import UserGet
from api.resources.sentotp import SentOTP
from api.resources.verify_account import VerifyAccount
from api.resources.reset_password import ResetPassword
from api.resources.forgot_password import ForgotPassword
from api.resources.post import PostResource, PostLikeResource
from api.resources.post_comment import PostCommentResource, CommentLike
from api.resources.post_comment_reply import PostCommentReplyResource, ReplyLike

user_blueprint = Blueprint("user", __name__, url_prefix="/user")
user_api = Api(user_blueprint, errors=user_blueprint.errorhandler)
user_api.add_resource(UserGet, "/", "/delete")


otp_blueprint = Blueprint("otp", __name__, url_prefix="/otp")
otp_api = Api(otp_blueprint, errors=otp_blueprint.errorhandler)
otp_api.add_resource(SentOTP, "/send-otp")


verify_ac_blueprint = Blueprint(
    "verify_account", __name__, url_prefix="/verify-account"
)
verify_ac_api = Api(verify_ac_blueprint, errors=verify_ac_blueprint.errorhandler)
verify_ac_api.add_resource(VerifyAccount, "/")


reset_password_blueprint = Blueprint(
    "reset_password", __name__, url_prefix="/reset-password"
)
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


posts_blueprint = Blueprint("posts", __name__, url_prefix="/posts")
posts_api = Api(posts_blueprint, errors=posts_blueprint.errorhandler)
posts_api.add_resource(PostResource, "/get-posts", "/create", "/update")

posts_like_blueprint = Blueprint("post_like", __name__, url_prefix="/posts")
posts_like_api = Api(posts_like_blueprint, errors=posts_like_blueprint.errorhandler)
posts_like_api.add_resource(PostLikeResource, "/like", "/dislike")

posts_comment_blueprint = Blueprint("post_comment", __name__, url_prefix="/posts")
posts_comment_api = Api(posts_comment_blueprint, errors=posts_comment_blueprint.errorhandler)
posts_comment_api.add_resource(PostCommentResource, "/comment", "/viewcomments", "/update-comment", "/delete-comment")

comment_like_blueprint = Blueprint("comment-like", __name__, url_prefix="/posts")
comment_like_api = Api(comment_like_blueprint, errors=comment_like_blueprint.errorhandler)
comment_like_api.add_resource(CommentLike, "/like-comment")

comment_reply_like_blueprint = Blueprint("comment-reply", __name__, url_prefix="/posts/comment")
comment_reply_like_api = Api(comment_reply_like_blueprint, errors=comment_reply_like_blueprint.errorhandler)
comment_reply_like_api.add_resource(PostCommentReplyResource, "/reply", "/viewreplies", "/update-reply", "/delete-reply")

reply_like_blueprint = Blueprint("reply-like", __name__, url_prefix="/posts")
reply_like_api = Api(reply_like_blueprint, errors=reply_like_blueprint.errorhandler)
reply_like_api.add_resource(ReplyLike, "/like-reply", "/dislike-reply")