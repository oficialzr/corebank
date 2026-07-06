from datetime import UTC, datetime

from corebank_api.repositories.transactions import save_transaction
from corebank_api.schemas.common import Currency
from corebank_api.schemas.transaction import TransactionResponse
from corebank_api.schemas.transfer import TransferStatus
from corebank_api.services.transactions import get_transaction, list_transactions


def test_list_transactions_service_returns_transactions() -> None:
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

    transactions = list_transactions()

    assert len(transactions) == 1
    assert transactions[0].id == "tx-001"


def test_get_transaction_service_returns_transaction_by_id() -> None:
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

    found_transaction = get_transaction("tx-001")

    assert found_transaction is not None
    assert found_transaction.id == "tx-001"


def test_get_transaction_service_returns_none_for_unknown_transaction() -> None:
    transaction = get_transaction("tx-999")

    assert transaction is None