"""v0_7

Revision ID: 8f074f67800a
Revises: dcfa09666e4d
Create Date: 2023-12-24 23:11:58.616143

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8f074f67800a'
down_revision: Union[str, None] = 'dcfa09666e4d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'is_archive')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('is_archive', sa.BOOLEAN(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
