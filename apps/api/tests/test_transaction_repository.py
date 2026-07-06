from datetime import UTC, datetime

from corebank_api.repositories.transactions import (
    generate_transaction_id,
    get_all_transactions,
    get_transaction_by_id,
    save_transaction,
)
from corebank_api.schemas.common import Currency
from corebank_api.schemas.transaction import TransactionResponse
from corebank_api.schemas.transfer import TransferStatus


def test_save_transaction_repository_saves_transaction() -> None:
    transaction = TransactionResponse(
        id="tx-001",
        from_account_id="acc-001",
        to_account_id="acc-002",
        amount=1000,
        currency=Currency.RUB,
        status=TransferStatus.COMPLETED,
        created_at=datetime.now(UTC),
    )

    save_transaction(transaction)

    transactions = get_all_transactions()

    assert len(transactions) == 1
    assert transactions[0].id == "tx-001"


def test_get_transaction_by_id_repository_returns_transaction() -> None:
    transaction = TransactionResponse(
        id="tx-001",
        from_account_id="acc-001",
        to_account_id="acc-002",
        amount=1000,
        currency=Currency.RUB,
        status=TransferStatus.COMPLETED,
        created_at=datetime.now(UTC),
    )

    save_transaction(transaction)

    found_transaction = get_transaction_by_id("tx-001")

    assert found_transaction is not None
    assert found_transaction.id == "tx-001"


def test_get_transaction_by_id_repository_returns_none_for_unknown_transaction() -> (
    None
):
    transaction = get_transaction_by_id("tx-999")

    assert transaction is None


def test_generate_transaction_id_repository_returns_next_id() -> None:
    first_transaction_id = generate_transaction_id()

    transaction = TransactionResponse(
        id=first_transaction_id,
        from_account_id="acc-001",
        to_account_id="acc-002",
        amount=1000,
        currency=Currency.RUB,
        status=TransferStatus.COMPLETED,
        created_at=datetime.now(UTC),
    )

    save_transaction(transaction)

    second_transaction_id = generate_transaction_id()

    assert first_transaction_id == "tx-001"
    assert second_transaction_id == "tx-002"
