"""add exercise language

Revision ID: 0007
Revises: 0006
Create Date: 2026-10-03

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0007"
down_revision: Union[str, None] = "0006"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "exercises",
        sa.Column("language", sa.String(20), nullable=False, server_default="python"),
    )


def downgrade() -> None:
    op.drop_column("exercises", "language")
