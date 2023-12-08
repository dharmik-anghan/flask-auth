from extentions import ma
from models.user import OTPDatabase
from marshmallow import EXCLUDE

class OTPSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OTPDatabase
        load_instance = True
        exclude = ["id"]
        include_fk = True