from flask import Flask
from extentions import db, jwt, oauth
from auth.views import auth_blueprint
from api.views import (
    user_blueprint,
    otp_blueprint,
    verify_ac_blueprint,
    reset_password_blueprint,
    forgot_password_blueprint,
    posts_blueprint,
    posts_like_blueprint,
    posts_comment_blueprint,
    comment_like_blueprint,
    comment_reply_like_blueprint,
    reply_like_blueprint
)
from google_auth.views import google_oauth
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
app.config.from_object(obj="config")

app.register_blueprint(blueprint=auth_blueprint)
app.register_blueprint(blueprint=user_blueprint)
app.register_blueprint(blueprint=otp_blueprint)
app.register_blueprint(blueprint=verify_ac_blueprint)
app.register_blueprint(blueprint=reset_password_blueprint)
app.register_blueprint(blueprint=forgot_password_blueprint)
app.register_blueprint(blueprint=google_oauth)
app.register_blueprint(blueprint=posts_blueprint)
app.register_blueprint(blueprint=posts_like_blueprint)
app.register_blueprint(blueprint=posts_comment_blueprint)
app.register_blueprint(blueprint=comment_like_blueprint)
app.register_blueprint(blueprint=comment_reply_like_blueprint)
app.register_blueprint(blueprint=reply_like_blueprint)

db.init_app(app=app)
jwt.init_app(app=app)
oauth.init_app(app=app)

oauth.register(
    name="google",
    server_metadata_url=os.environ.get("CONF_URL"),
    client_kwargs={"scope": "openid email profile"},
)

app.app_context().push()


if __name__ == "__main__":
    app.run(
        host=app.config.get("FLASK_RUN_HOST"),
        port=app.config.get("FLASK_RUN_PORT"),
    )
