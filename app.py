from flask import Flask
from extentions import db, jwt
from auth.views import auth_blueprint
from api.views import (
    user_blueprint,
    otp_blueprint,
    verify_ac_blueprint,
    reset_password_blueprint,
    forgot_password_blueprint,
)

app = Flask(__name__)
app.config.from_object(obj="config")

app.register_blueprint(blueprint=auth_blueprint)
app.register_blueprint(blueprint=user_blueprint)
app.register_blueprint(blueprint=otp_blueprint)
app.register_blueprint(blueprint=verify_ac_blueprint)
app.register_blueprint(blueprint=reset_password_blueprint)
app.register_blueprint(blueprint=forgot_password_blueprint)

db.init_app(app=app)
jwt.init_app(app=app)
app.app_context().push()


if __name__ == "__main__":
    app.run(
        host=app.config.get("FLASK_RUN_HOST"),
        port=app.config.get("FLASK_RUN_PORT"),
    )
