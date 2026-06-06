"""drop item_id FK from character_equipment

Revision ID: 007_drop_item_id_fk
Revises: 006_add_name_kr_to_encounters
Create Date: 2026-06-06

"""
from typing import Sequence, Union
from alembic import op

revision: str = '007_drop_item_id_fk'
down_revision: Union[str, None] = 'b7d4c2e91a05'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('character_equipment') as batch_op:
        batch_op.drop_constraint('character_equipment_item_id_fkey', type_='foreignkey')


def downgrade() -> None:
    pass
