"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-01-01 00:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("username", sa.String(50), nullable=False, unique=True, index=True),
        sa.Column("email", sa.String(255), nullable=False, unique=True, index=True),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("total_score", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("streak", sa.Integer(), nullable=False, server_default="0"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
    )

    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("name", sa.String(100), nullable=False, unique=True),
        sa.Column("slug", sa.String(100), nullable=False, unique=True),
    )

    difficulty_enum = sa.Enum(
        "beginner", "intermediate", "advanced", name="difficultylevel"
    )
    op.create_table(
        "exercises",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("hint", sa.Text(), nullable=True),
        sa.Column("difficulty_level", difficulty_enum, nullable=False, server_default="beginner"),
        sa.Column("category_id", sa.Integer(), sa.ForeignKey("categories.id"), nullable=True),
        sa.Column("starter_code", sa.Text(), server_default=""),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
    )

    op.create_table(
        "test_cases",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("exercise_id", sa.Integer(), sa.ForeignKey("exercises.id"), nullable=False),
        sa.Column("input_data", sa.Text(), server_default=""),
        sa.Column("expected_output", sa.Text(), nullable=False),
        sa.Column("score_weight", sa.Float(), server_default="1.0"),
        sa.Column("is_hidden", sa.Boolean(), server_default="false"),
    )

    status_enum = sa.Enum("pending", "completed", "failed", name="submissionstatus")
    op.create_table(
        "submissions",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("exercise_id", sa.Integer(), sa.ForeignKey("exercises.id"), nullable=False),
        sa.Column("code", sa.Text(), nullable=False),
        sa.Column("status", status_enum, server_default="pending"),
        sa.Column("score", sa.Float(), server_default="0.0"),
        sa.Column("stdout", sa.Text(), server_default=""),
        sa.Column("stderr", sa.Text(), server_default=""),
        sa.Column("time_taken_ms", sa.Integer(), server_default="0"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
    )


def downgrade() -> None:
    op.drop_table("submissions")
    op.drop_table("test_cases")
    op.drop_table("exercises")
    op.drop_table("categories")
    op.drop_table("users")
    sa.Enum(name="submissionstatus").drop(op.get_bind())
    sa.Enum(name="difficultylevel").drop(op.get_bind())
