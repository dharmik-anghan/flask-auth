"""v0_1

Revision ID: 79de8bc67179
Revises: 
Create Date: 2023-12-22 10:26:19.242500

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '79de8bc67179'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('full_name', sa.String(length=40), nullable=False),
    sa.Column('username', sa.String(length=15), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('is_public', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_deleted', sa.Boolean(), nullable=False),
    sa.Column('is_social', sa.Boolean(), nullable=False),
    sa.Column('following_count', sa.Integer(), nullable=True),
    sa.Column('follower_count', sa.Integer(), nullable=True),
    sa.Column('post_count', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('modified_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('followers_followings',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('followed_by', sa.Integer(), nullable=False),
    sa.Column('followed_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['followed_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_followers_followings_followed_by'), 'followers_followings', ['followed_by'], unique=False)
    op.create_index(op.f('ix_followers_followings_user_id'), 'followers_followings', ['user_id'], unique=False)
    op.create_table('otpdatabase',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('otp', sa.String(), nullable=False),
    sa.Column('otp_received_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('posts',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('post', sa.String(), nullable=False),
    sa.Column('caption', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('modified_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('like_count', sa.Integer(), nullable=True),
    sa.Column('comment_count', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_posts_user_id'), 'posts', ['user_id'], unique=False)
    op.create_table('token_block_list',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('jti', sa.String(), nullable=False),
    sa.Column('token_type', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('revoked_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('expires', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_token_block_list_user_id'), 'token_block_list', ['user_id'], unique=False)
    op.create_table('post_comments',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('comment', sa.String(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('modified_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('comment_like_count', sa.Integer(), nullable=True),
    sa.Column('comment_reply_count', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_post_comments_post_id'), 'post_comments', ['post_id'], unique=False)
    op.create_index(op.f('ix_post_comments_user_id'), 'post_comments', ['user_id'], unique=False)
    op.create_table('post_likes',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('liked_by', sa.Integer(), nullable=False),
    sa.Column('liked_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['liked_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comment_likes',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('comment_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['comment_id'], ['post_comments.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment_likes')
    op.drop_table('post_likes')
    op.drop_index(op.f('ix_post_comments_user_id'), table_name='post_comments')
    op.drop_index(op.f('ix_post_comments_post_id'), table_name='post_comments')
    op.drop_table('post_comments')
    op.drop_index(op.f('ix_token_block_list_user_id'), table_name='token_block_list')
    op.drop_table('token_block_list')
    op.drop_index(op.f('ix_posts_user_id'), table_name='posts')
    op.drop_table('posts')
    op.drop_table('otpdatabase')
    op.drop_index(op.f('ix_followers_followings_user_id'), table_name='followers_followings')
    op.drop_index(op.f('ix_followers_followings_followed_by'), table_name='followers_followings')
    op.drop_table('followers_followings')
    op.drop_table('users')
    # ### end Alembic commands ###
