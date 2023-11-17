"""add name

Revision ID: b36576ba07ec
Revises: 13d511b20195
Create Date: 2023-11-17 12:08:09.330552

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b36576ba07ec'
down_revision: Union[str, None] = '13d511b20195'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('name', sa.String(), nullable=True))
    pass


def downgrade() -> None:
    op.drop_column('users', 'users')
    pass
