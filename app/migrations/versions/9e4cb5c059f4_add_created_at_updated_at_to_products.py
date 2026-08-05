"""add_created_at_updated_at_to_products

Revision ID: 9e4cb5c059f4
Revises: 4ad07346c92a
Create Date: 2026-08-05 16:52:16.922572

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '9e4cb5c059f4'
down_revision: Union[str, Sequence[str], None] = '4ad07346c92a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('products', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False))
    op.add_column('products', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
    op.alter_column('users', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.DateTime(timezone=True),
               nullable=False)
    op.alter_column('users', 'updated_at',
               existing_type=postgresql.TIMESTAMP(),
               type_=sa.DateTime(timezone=True),
               existing_nullable=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('users', 'updated_at',
               existing_type=sa.DateTime(timezone=True),
               type_=postgresql.TIMESTAMP(),
               existing_nullable=True)
    op.alter_column('users', 'created_at',
               existing_type=sa.DateTime(timezone=True),
               type_=postgresql.TIMESTAMP(),
               nullable=True)
    op.drop_column('products', 'updated_at')
    op.drop_column('products', 'created_at')
