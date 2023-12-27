from extentions import ma
from models.post_comment_likes import PostCommentLikes


class PostCommentLikeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PostCommentLikes
        load_instance = True


class PostCommentLikeCreateSchema(PostCommentLikeSchema):
    class Meta(PostCommentLikeSchema.Meta):
        fields = [
            "comment_id",
            "post_id",
            "user_id",
        ]
class PostReplyLikeCreateSchema(PostCommentLikeSchema):
    class Meta(PostCommentLikeSchema.Meta):
        fields = [
            "comment_id",
            "post_id",
            "user_id",
            "reply_id",
        ]


class PostCommentLikeResponseSchema(PostCommentLikeSchema):
    class Meta(PostCommentLikeSchema.Meta):
        fields = [
            "id",
            "comment_id",
            "reply_id",
            "post_id",
            "user_id",
            "created_at",
        ]
