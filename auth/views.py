from flask import request, jsonify, Blueprint
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from auth.helpers import add_token_to_database
from flask import current_app as app
from api.schemas.user import UserCreateSchema, UserSchema
from extentions import pwd_context, jwt, db
from models.user import User

auth_blueprint = Blueprint("auth", __name__, url_prefix="/auth")


@auth_blueprint.route("/register", methods=["POST"])
def register():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400 
    
    schema = UserCreateSchema()
    user = schema.load(request.json)
    db.session.add(user)
    db.session.commit()

    schema = UserSchema()

    return {"msg": "User Created", "user": schema.dump(user)}

@auth_blueprint.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    
    email = request.json.get("email")
    password = request.json.get("password")

    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400    

    user = User.query.filter_by(email=email).first()

    if user is None or not pwd_context.verify(password, user.password):
        return jsonify({"msg": "Bad credentials"}), 400
    
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    add_token_to_database(access_token)

    return jsonify({"access_token": access_token, "refresh_token": refresh_token})
