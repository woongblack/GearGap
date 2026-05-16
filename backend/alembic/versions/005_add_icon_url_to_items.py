"""add_icon_url_to_items

Revision ID: a3f8e1c92b74
Revises: 004b09dd9606
Create Date: 2026-05-17 00:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = 'a3f8e1c92b74'
down_revision: Union[str, None] = '004b09dd9606'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('items') as batch_op:
        batch_op.add_column(sa.Column('icon_url', sa.String(300), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table('items') as batch_op:
        batch_op.drop_column('icon_url')
