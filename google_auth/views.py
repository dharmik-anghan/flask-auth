from flask import url_for, session, redirect, Blueprint, jsonify
from extentions import oauth, db
from models.user import User
from api.schemas.user import UserCreateSchema, UserSchema
from random import randint, choice

google_oauth = Blueprint("google_oauth", __name__, url_prefix="/auth/google")


@google_oauth.route("/login")
def google_login():
    redirect_uri = url_for("google_oauth.auth", _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@google_oauth.route("/callback")
def auth():
    token = oauth.google.authorize_access_token()
    session["user"] = token["userinfo"]
    user = session.get("userinfo")

    return redirect(url_for("google_oauth.register"))


@google_oauth.get("/register")
def register():
    user = session.get("user")

    db_user = User.query.filter_by(email=user["email"]).first()

    if db_user:
        return jsonify({"msg": "Email already registered"})

    temp_user = {}
    user = jsonify(user)
    user = user.get_json()
    username = user.get("email").split("@")
    password = (
        (username[0][:3])
        + (f"{choice(seq=['@', '#', '^', '&', '$'])}")
        + (f"{randint(10000,100000)}")
        + f"{choice(list('QWERTYUIOPLKJHGFDASZXCVBNM'))}"
    )

    temp_user["email"] = user.get("email")
    temp_user["full_name"] = user.get("name")
    temp_user["password"] = password
    temp_user["username"] = username[0]
    temp_user["is_verified"] = True if user.get("email_verified") == True else False

    schema = UserCreateSchema()
    db_user = schema.load(temp_user)
    db.session.add(db_user)
    db.session.commit()

    schema = UserSchema()

    return {
        "msg": "User Created",
        "user": temp_user,
        "security_alert": f"{password}, This is your system generated password, change it as soon as possible",
    }


@google_oauth.route("/logout")
def logout():
    session.pop("user", None)
    return jsonify({"msg": "Logged Out!!!"})
