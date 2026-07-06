import pytest
from corebank_api.domain.errors import (
    CurrencyMismatchError,
    DestinationAccountNotFoundError,
    InsufficientFundsError,
    SameAccountTransferError,
    SourceAccountNotFoundError,
)
from corebank_api.repositories.accounts_provider import get_account_by_id
from corebank_api.repositories.transactions_provider import get_transaction_by_id
from corebank_api.schemas.account import AccountCreateRequest
from corebank_api.schemas.transfer import TransferCreateRequest
from corebank_api.services.accounts import create_account
from corebank_api.services.transfers import create_transfer


def assert_transaction_id_format(transaction_id: str) -> None:
    assert transaction_id.startswith("tx-")
    assert len(transaction_id) > len("tx-")


def test_create_transfer_service_moves_money_between_accounts() -> None:
    request = TransferCreateRequest(
        from_account_id="acc-001",
        to_account_id="acc-002",
        amount=1000,
    )

    response = create_transfer(request)

    transaction = get_transaction_by_id(response.transaction_id)
    from_account = get_account_by_id("acc-001")
    to_account = get_account_by_id("acc-002")

    assert transaction is not None
    assert transaction.created_at is not None

    assert_transaction_id_format(response.transaction_id)
    assert response.from_account_id == "acc-001"
    assert response.to_account_id == "acc-002"
    assert response.amount == 1000
    assert response.status == "completed"

    assert from_account is not None
    assert to_account is not None
    assert from_account.balance == 99000
    assert to_account.balance == 51000


def test_create_transfer_service_raises_404_for_unknown_source_account() -> None:
    request = TransferCreateRequest(
        from_account_id="acc-999",
        to_account_id="acc-002",
        amount=1000,
    )

    with pytest.raises(SourceAccountNotFoundError):
        create_transfer(request)


def test_create_transfer_service_raises_404_for_unknown_destination_account() -> None:
    request = TransferCreateRequest(
        from_account_id="acc-001",
        to_account_id="acc-999",
        amount=1000,
    )

    with pytest.raises(DestinationAccountNotFoundError):
        create_transfer(request)


def test_create_transfer_service_rejects_transfer_to_same_account() -> None:
    request = TransferCreateRequest(
        from_account_id="acc-001",
        to_account_id="acc-001",
        amount=1000,
    )

    with pytest.raises(SameAccountTransferError):
        create_transfer(request)


def test_create_transfer_service_rejects_insufficient_funds() -> None:
    request = TransferCreateRequest(
        from_account_id="acc-001",
        to_account_id="acc-002",
        amount=999999999,
    )

    with pytest.raises(InsufficientFundsError):
        create_transfer(request)


def test_create_transfer_service_rejects_currency_mismatch() -> None:
    usd_account = create_account(
        AccountCreateRequest(
            owner_name="Usd User",
            currency="USD",
        ),
    )

    request = TransferCreateRequest(
        from_account_id="acc-001",
        to_account_id=usd_account.id,
        amount=1000,
    )

    with pytest.raises(CurrencyMismatchError):
        create_transfer(request)


def test_create_transfer_service_rolls_back_when_transaction_save_fails(
    monkeypatch,
) -> None:
    def broken_save_transaction(*args, **kwargs):
        raise RuntimeError("transaction save failed")

    monkeypatch.setattr(
        "corebank_api.services.transfers.sql_transactions.save_transaction",
        broken_save_transaction,
    )

    request = TransferCreateRequest(
        from_account_id="acc-001",
        to_account_id="acc-002",
        amount=1000,
    )

    with pytest.raises(RuntimeError):
        create_transfer(request)

    from_account = get_account_by_id("acc-001")
    to_account = get_account_by_id("acc-002")

    assert from_account is not None
    assert to_account is not None
    assert from_account.balance == 100000
    assert to_account.balance == 50000
