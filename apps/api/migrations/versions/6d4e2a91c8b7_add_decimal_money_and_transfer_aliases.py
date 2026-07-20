"""add decimal money and transfer aliases

Revision ID: 6d4e2a91c8b7
Revises: f120dc63a1d4
Create Date: 2026-07-20 12:00:00.000000

"""

import hashlib
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "6d4e2a91c8b7"
down_revision: str | Sequence[str] | None = "f120dc63a1d4"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def add_luhn_check_digit(number: str) -> str:
    total = 0
    parity = (len(number) + 1) % 2

    for index, character in enumerate(number):
        digit = int(character)
        if index % 2 == parity:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit

    return f"{number}{(10 - total % 10) % 10}"


def card_number_for_account(account_id: str, salt: int = 0) -> str:
    digest = hashlib.sha256(f"{account_id}:{salt}".encode()).hexdigest()
    body = f"2200{int(digest[:16], 16) % 10**11:011d}"
    return add_luhn_check_digit(body)


def upgrade() -> None:
    op.add_column("users", sa.Column("phone_number", sa.String(length=16), nullable=True))
    op.create_unique_constraint("uq_users_phone_number", "users", ["phone_number"])

    op.add_column("accounts", sa.Column("card_number", sa.String(length=16), nullable=True))

    connection = op.get_bind()
    account_ids = connection.execute(sa.text("SELECT id FROM accounts ORDER BY id")).scalars()
    used_numbers: set[str] = set()

    for account_id in account_ids:
        salt = 0
        card_number = card_number_for_account(account_id, salt)
        while card_number in used_numbers:
            salt += 1
            card_number = card_number_for_account(account_id, salt)
        used_numbers.add(card_number)
        connection.execute(
            sa.text("UPDATE accounts SET card_number = :card_number WHERE id = :account_id"),
            {"card_number": card_number, "account_id": account_id},
        )

    op.alter_column("accounts", "card_number", nullable=False)
    op.create_unique_constraint("uq_accounts_card_number", "accounts", ["card_number"])
    op.create_index("ix_accounts_card_number", "accounts", ["card_number"])

    op.alter_column(
        "accounts",
        "balance",
        type_=sa.Numeric(18, 2),
        postgresql_using="balance::numeric / 100",
    )
    op.alter_column(
        "transactions",
        "amount",
        type_=sa.Numeric(18, 2),
        postgresql_using="amount::numeric / 100",
    )


def downgrade() -> None:
    op.alter_column(
        "transactions",
        "amount",
        type_=sa.Integer(),
        postgresql_using="round(amount * 100)::integer",
    )
    op.alter_column(
        "accounts",
        "balance",
        type_=sa.Integer(),
        postgresql_using="round(balance * 100)::integer",
    )
    op.drop_index("ix_accounts_card_number", table_name="accounts")
    op.drop_constraint("uq_accounts_card_number", "accounts", type_="unique")
    op.drop_column("accounts", "card_number")
    op.drop_constraint("uq_users_phone_number", "users", type_="unique")
    op.drop_column("users", "phone_number")
