from flask import url_for, session, redirect, Blueprint, jsonify
from extentions import oauth, db
from models.user import User
from api.schemas.user import UserCreateSchema, UserSchema

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

    return {"msg": "User Created", "user": user}


@google_oauth.route("/logout")
def logout():
    session.pop("user", None)
    return jsonify({"msg": "Logged Out!!!"})
