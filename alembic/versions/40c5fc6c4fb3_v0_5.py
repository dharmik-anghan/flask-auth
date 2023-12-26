"""v0_5

Revision ID: 40c5fc6c4fb3
Revises: bf384107d271
Create Date: 2023-12-24 21:28:17.946797

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '40c5fc6c4fb3'
down_revision: Union[str, None] = 'bf384107d271'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('follower_count', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('following_count', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('post_count', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'post_count')
    op.drop_column('users', 'following_count')
    op.drop_column('users', 'follower_count')
    # ### end Alembic commands ###
