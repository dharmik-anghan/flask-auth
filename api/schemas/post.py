from extentions import ma
from models.post import Post


class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        load_instance = True


class PostCreateSchema(PostSchema):
    class Meta(PostSchema.Meta):
        fields = [
            "user_id",
            "post",
            "caption",
        ]  # Include the fields relevant to Post creation


class PostUpdateSchema(PostSchema):
    class Meta(PostSchema.Meta):
        fields = ["caption"]  # Include the fields relevant to Post creation


class PostResponseSchema(PostSchema):
    class Meta:
        fields = [
            "id",
            "user_id",
            "post",
            "created_at",
            "like_count",
            "comment_count",
            "caption",
        ]
