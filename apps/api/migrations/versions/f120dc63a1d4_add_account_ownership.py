"""add account ownership

Revision ID: f120dc63a1d4
Revises: 3b6991cd9993
Create Date: 2026-07-16 12:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


revision: str = "f120dc63a1d4"
down_revision: Union[str, Sequence[str], None] = "3b6991cd9993"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Existing accounts cannot be assigned safely without an explicit owner.
    # They remain unassigned and are hidden by all user-scoped API queries.
    op.add_column("accounts", sa.Column("user_id", sa.String(), nullable=True))
    op.create_foreign_key(
        "fk_accounts_user_id_users",
        "accounts",
        "users",
        ["user_id"],
        ["id"],
        ondelete="RESTRICT",
    )
    op.create_index("ix_accounts_user_id", "accounts", ["user_id"])


def downgrade() -> None:
    op.drop_index("ix_accounts_user_id", table_name="accounts")
    op.drop_constraint("fk_accounts_user_id_users", "accounts", type_="foreignkey")
    op.drop_column("accounts", "user_id")
