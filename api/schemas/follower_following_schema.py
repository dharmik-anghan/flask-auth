from extentions import ma
from models.user_request import RequestToUser
from models.follower_following import FollowerFollowing


class FollowerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = FollowerFollowing
        load_instance = True


class RequestSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RequestToUser
        load_instance = True


class CreateFollowerSchema(FollowerSchema):
    class Meta(FollowerSchema.Meta):
        fields = ["followed_to", "followed_by"]


class CreateRequestSchema(RequestSchema):
    class Meta(RequestSchema.Meta):
        fields = ["requested_to", "requested_by"]

class RequestResponseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        fields = ["requested_by", "created_at"]

