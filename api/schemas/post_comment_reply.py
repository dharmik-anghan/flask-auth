from extentions import ma
from models.post_comment_reply import PostCommentReply


class PostCommentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PostCommentReply
        load_instance = True


class PostCreateCommentSchema(PostCommentSchema):
    class Meta(PostCommentSchema.Meta):
        fields = ["post_id", "comment_reply", "user_id", "comment_id"]


class PostCommentReplyResponseSchema(PostCommentSchema):
    class Meta(PostCommentSchema.Meta):
        fields = [
            "id",
            "post_id",
            "comment_id",
            "comment_reply",
            "user_id",
            "created_at",
            "modified_at",
            "reply_like_count",
        ]
