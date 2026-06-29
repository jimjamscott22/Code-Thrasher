"""add resources table

Revision ID: 0006
Revises: 71d51bde7666
Create Date: 2026-06-13

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0006"
down_revision: Union[str, None] = "0005"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    difficulty_enum = postgresql.ENUM(
        "beginner", "intermediate", "advanced", name="difficultylevel", create_type=False
    )
    op.create_table(
        "resources",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("slug", sa.String(200), nullable=False),
        sa.Column("topic_area", sa.String(100), nullable=False),
        sa.Column("difficulty_level", difficulty_enum, nullable=False, server_default="beginner"),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("sections", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug"),
    )
    op.create_index(op.f("ix_resources_id"), "resources", ["id"], unique=False)
    op.create_index(op.f("ix_resources_slug"), "resources", ["slug"], unique=True)
    op.create_index(op.f("ix_resources_topic_area"), "resources", ["topic_area"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_resources_topic_area"), table_name="resources")
    op.drop_index(op.f("ix_resources_slug"), table_name="resources")
    op.drop_index(op.f("ix_resources_id"), table_name="resources")
    op.drop_table("resources")
