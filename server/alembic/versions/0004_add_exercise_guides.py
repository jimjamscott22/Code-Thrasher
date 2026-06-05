"""add_exercise_guides

Revision ID: 0004
Revises: 0003
Create Date: 2026-06-04 22:38:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0004"
down_revision: Union[str, None] = "0003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "exercises",
        sa.Column("guide", sa.JSON(), nullable=False, server_default=sa.text("'[]'")),
    )
    op.add_column("exercises", sa.Column("solution_code", sa.Text(), nullable=True))
    op.add_column("exercises", sa.Column("solution_explanation", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("exercises", "solution_explanation")
    op.drop_column("exercises", "solution_code")
    op.drop_column("exercises", "guide")
