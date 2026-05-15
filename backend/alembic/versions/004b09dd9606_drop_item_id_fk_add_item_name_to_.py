"""add_item_name_to_character_equipment

Revision ID: 004b09dd9606
Revises: 50a67e541212
Create Date: 2026-05-16 05:41:11.439885

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = '004b09dd9606'
down_revision: Union[str, None] = '50a67e541212'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # item_id → items.id FK는 DB에 원래부터 없었음 — drop_constraint 불필요.
    # item_name 컬럼만 추가.
    with op.batch_alter_table('character_equipment') as batch_op:
        batch_op.add_column(sa.Column('item_name', sa.String(), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table('character_equipment') as batch_op:
        batch_op.drop_column('item_name')
