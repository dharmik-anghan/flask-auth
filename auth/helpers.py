from extentions import db
from models.auth import TokenBlockList
from flask import current_app as app
from flask_jwt_extended import decode_token
from datetime import datetime

def add_token_to_database(encoded_token):
    decoded_token = decode_token(encoded_token=encoded_token)
    jti = decoded_token["jti"]
    token_type = decoded_token["type"]
    user_id = decoded_token[app.config["JWT_IDENTITY_CLAIM"]]
    expires = datetime.fromtimestamp(decoded_token["exp"])

    db_token = TokenBlockList(
        jti=jti,
        expires=expires,
        token_type=token_type,
        user_id=user_id
    )

    db.session.add(db_token)
    db.session.commit()