"""update users table: rename name to first_name, add last_name birth_date phone_number

Revision ID: 3b0510f26361
Revises: d571e090dd58
Create Date: 2026-01-15 13:52:05.220523

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3b0510f26361'
down_revision: Union[str, Sequence[str], None] = 'd571e090dd58'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('ALTER TABLE users RENAME COLUMN name TO first_name')
    op.add_column('users', sa.Column('last_name', sa.String(), nullable=True))
    op.add_column('users', sa.Column('birth_date', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'phone_number')
    op.drop_column('users', 'birth_date')
    op.drop_column('users', 'last_name')
    op.execute('ALTER TABLE users RENAME COLUMN first_name TO name')
