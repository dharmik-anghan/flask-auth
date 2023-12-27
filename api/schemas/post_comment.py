from extentions import ma
from models.post_comments import PostComment


class PostCommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PostComment
        load_instance = True


class PostCreateCommentSchema(PostCommentSchema):
    class Meta(PostCommentSchema.Meta):
        fields = ["post_id", "comment", "user_id"]


class PostCommentResponseSchema(PostCommentSchema):
    class Meta(PostCommentSchema.Meta):
        fields = [
            "id",
            "post_id",
            "comment",
            "user_id",
            "created_at",
            "modified_at",
            "comment_like_count",
            "comment_reply_count"
        ]
