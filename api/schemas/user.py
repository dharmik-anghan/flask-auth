from extentions import ma
from models.user import User
from marshmallow.fields import String, Boolean
from marshmallow import validate, ValidationError, validates_schema


class UserSchema(ma.SQLAlchemyAutoSchema):
    email = String(required=True, validate=[validate.Email()])

    @validates_schema
    def validate_email(self, data, **kwargs):
        email = data.get("email")

        if User.query.filter_by(email=email).count():
            raise ValidationError(f"email {email} already exists.")

    class Meta:
        model = User
        load_instance = True
        exclude = ["_password", "is_deleted", "modified_at", "is_active"]


class UserCreateSchema(UserSchema):
    password = String(
        required=True,
        validate=[
            validate.Regexp(
                r"^(?=.*[A-Z])(?=.*[!@#$&*])(?=.*[0-9])(?=.*[a-z]).{8,}$",
                error="The password need to be at least 8 characters long, and have at least 1 of each of the following: lowercase letter, uppercase letter, special character, number.",
            )
        ],
    )
    is_public = Boolean(required=True)

class UserRequestSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        fields= ["id", "username", "full_name", "follower_count", "following_count", "post_count"]
