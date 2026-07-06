from datetime import UTC, datetime

from corebank_api.repositories import transactions_provider
from corebank_api.schemas.common import Currency
from corebank_api.schemas.transaction import TransactionResponse
from corebank_api.schemas.transfer import TransferStatus


def test_transactions_provider_uses_memory_backend_by_default(monkeypatch) -> None:
    monkeypatch.delenv("COREBANK_REPOSITORY_BACKEND", raising=False)

    first_transaction_id = transactions_provider.generate_transaction_id()

    transaction = TransactionResponse(
        id=first_transaction_id,
        from_account_id="acc-provider-001",
        to_account_id="acc-provider-002",
        amount=1000,
        currency=Currency.RUB,
        status=TransferStatus.COMPLETED,
        created_at=datetime.now(UTC),
    )

    transactions_provider.save_transaction(transaction)

    found_transaction = transactions_provider.get_transaction_by_id(
        first_transaction_id
    )
    account_transactions = transactions_provider.get_transactions_by_account_id(
        "acc-provider-001"
    )
    all_transactions = transactions_provider.get_all_transactions()
    second_transaction_id = transactions_provider.generate_transaction_id()

    assert found_transaction is not None
    assert found_transaction.id == first_transaction_id
    assert len(account_transactions) == 1
    assert account_transactions[0].id == first_transaction_id
    assert any(tx.id == first_transaction_id for tx in all_transactions)
    assert first_transaction_id == "tx-001"
    assert second_transaction_id == "tx-002"