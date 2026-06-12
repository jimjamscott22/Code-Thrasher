"""add user is_admin and solution_reveals table

Revision ID: 0005
Revises: 0004
Create Date: 2026-06-11

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0005"
down_revision: Union[str, None] = "0004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("is_admin", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.create_table(
        "solution_reveals",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("exercise_id", sa.Integer(), nullable=False),
        sa.Column("revealed_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["exercise_id"], ["exercises.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "exercise_id", name="uq_solution_reveal_user_exercise"),
    )
    op.create_index(op.f("ix_solution_reveals_id"), "solution_reveals", ["id"], unique=False)
    op.create_index(op.f("ix_solution_reveals_user_id"), "solution_reveals", ["user_id"], unique=False)
    op.create_index(op.f("ix_solution_reveals_exercise_id"), "solution_reveals", ["exercise_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_solution_reveals_exercise_id"), table_name="solution_reveals")
    op.drop_index(op.f("ix_solution_reveals_user_id"), table_name="solution_reveals")
    op.drop_index(op.f("ix_solution_reveals_id"), table_name="solution_reveals")
    op.drop_table("solution_reveals")
    op.drop_column("users", "is_admin")
