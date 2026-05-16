"""add_name_kr_to_encounters

Revision ID: b7d4c2e91a05
Revises: a3f8e1c92b74
Create Date: 2026-05-17 00:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = 'b7d4c2e91a05'
down_revision: Union[str, None] = 'a3f8e1c92b74'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('encounters') as batch_op:
        batch_op.add_column(sa.Column('name_kr', sa.String(), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table('encounters') as batch_op:
        batch_op.drop_column('name_kr')
