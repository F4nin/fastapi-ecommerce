"""add token_version and timestamps to users

Revision ID: 14bcb1f0be3c
Revises: b592b170e454
Create Date: 2026-08-04 12:35:00
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers
revision: str = '14bcb1f0be3c'
down_revision: Union[str, None] = 'b592b170e454'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Добавляем колонки как NULLABLE (разрешаем NULL)
    op.add_column('users', sa.Column('token_version', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('updated_at', sa.DateTime(), nullable=True))

    # 2. Заполняем существующие записи значениями по умолчанию
    op.execute("UPDATE users SET token_version = 0 WHERE token_version IS NULL")
    op.execute("UPDATE users SET created_at = NOW() WHERE created_at IS NULL")
    op.execute("UPDATE users SET updated_at = NOW() WHERE updated_at IS NULL")

    # 3. Делаем колонки NOT NULL
    op.alter_column('users', 'token_version', nullable=False)
    op.alter_column('users', 'created_at', nullable=False)
    op.alter_column('users', 'updated_at', nullable=False)


def downgrade() -> None:
    op.drop_column('users', 'updated_at')
    op.drop_column('users', 'created_at')
    op.drop_column('users', 'token_version')