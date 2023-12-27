from extentions import ma
from models.user import OTPDatabase


class OTPSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = OTPDatabase
        load_instance = True
        exclude = ["id"]
        include_fk = True
