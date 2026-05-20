"""make_submission_user_id_nullable

Revision ID: 0003
Revises: 71d51bde7666
Create Date: 2026-05-20 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '0003'
down_revision: Union[str, None] = '71d51bde7666'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('submissions', 'user_id',
                    existing_type=sa.Integer(),
                    nullable=True)


def downgrade() -> None:
    op.alter_column('submissions', 'user_id',
                    existing_type=sa.Integer(),
                    nullable=False)
