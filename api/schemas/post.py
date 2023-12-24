from extentions import ma
from models.post import Post
from marshmallow import fields


class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        load_instance = True
        # exclude  = ["id", "post", "user_id", "created_at", "like_count", "comment_count"]
        fields = ["post", "caption"]


class PostCreateSchema(PostSchema):
    class Meta(PostSchema.Meta):
        fields = ["user_id", "post", "caption"]  # Include the fields relevant to Post creation
    


class PostResponseSchema(PostSchema):
    class Meta:
        fields = ["id", "user_id", "post", "created_at", "like_count", "comment_count", "caption"]
