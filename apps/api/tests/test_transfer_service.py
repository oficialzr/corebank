import pytest
from corebank_api.domain.errors import (
    CurrencyMismatchError,
    DestinationAccountNotFoundError,
    InsufficientFundsError,
    SameAccountTransferError,
    SourceAccountNotFoundError,
)
from corebank_api.repositories.accounts import get_account_by_id
from corebank_api.schemas.account import AccountCreateRequest
from corebank_api.schemas.transfer import TransferCreateRequest
from corebank_api.services.accounts import create_account
from corebank_api.services.transfers import create_transfer


def test_create_transfer_service_moves_money_between_accounts() -> None:
    request = TransferCreateRequest(
        from_account_id="acc-001",
        to_account_id="acc-002",
        amount=1000,
    )

    response = create_transfer(request)

    from_account = get_account_by_id("acc-001")
    to_account = get_account_by_id("acc-002")

    assert response.from_account_id == "acc-001"
    assert response.to_account_id == "acc-002"
    assert response.amount == 1000
    assert response.status == "completed"

    assert from_account is not None
    assert to_account is not None
    assert from_account.balance == 99000
    assert to_account.balance == 251000


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
