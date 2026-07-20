"""add transfer idempotency

Revision ID: a7f3c29e10d5
Revises: 6d4e2a91c8b7
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "a7f3c29e10d5"
down_revision: str | Sequence[str] | None = "6d4e2a91c8b7"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "transfer_idempotency",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("idempotency_key", sa.String(length=128), nullable=False),
        sa.Column("request_hash", sa.String(length=64), nullable=False),
        sa.Column("transaction_id", sa.String(), nullable=True),
        sa.Column("from_account_id", sa.String(), nullable=True),
        sa.Column("to_account_id", sa.String(), nullable=True),
        sa.Column("amount", sa.Numeric(18, 2), nullable=True),
        sa.Column("status", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "idempotency_key", name="uq_transfer_idempotency_user_key"),
    )


def downgrade() -> None:
    op.drop_table("transfer_idempotency")
