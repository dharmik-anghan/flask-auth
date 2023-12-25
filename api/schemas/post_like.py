from extentions import ma
from datetime import datetime, timezone
from models.post_likes import PostLike

class PostLikeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PostLike
        load_instance=True

class PostLikeCreateSchema(PostLikeSchema):
    class Meta(PostLikeSchema.Meta):
        fields = ["post_id", "liked_by"]