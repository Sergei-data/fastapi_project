"""remove supplier_id from pet_categories

Revision ID: e1757cf69087
Revises: 61a81dffe5a1
Create Date: 2025-06-30 20:54:20.792281

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e1757cf69087'
down_revision: Union[str, Sequence[str], None] = '61a81dffe5a1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('pets_supplier_id_fkey'), 'pets', type_='foreignkey')
    op.drop_column('pets', 'supplier_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pets', sa.Column('supplier_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key(op.f('pets_supplier_id_fkey'), 'pets', 'users', ['supplier_id'], ['id'])
    # ### end Alembic commands ###
