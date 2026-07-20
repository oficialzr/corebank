"""add admin role

Revision ID: d8a91f2c4e60
Revises: c1d4e8a72b90
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "d8a91f2c4e60"
down_revision: str | Sequence[str] | None = "c1d4e8a72b90"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("is_admin", sa.Boolean(), server_default=sa.false(), nullable=False),
    )
    op.alter_column("users", "is_admin", server_default=None)


def downgrade() -> None:
    op.drop_column("users", "is_admin")
