import pytest
from corebank_api.repositories.accounts import get_account_by_id
from corebank_api.schemas.transfer import TransferCreateRequest
from corebank_api.services.transfers import create_transfer
from fastapi import HTTPException


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

    with pytest.raises(HTTPException) as error:
        create_transfer(request)

    assert error.value.status_code == 404
    assert error.value.detail == "Source account not found"


def test_create_transfer_service_raises_404_for_unknown_destination_account() -> None:
    request = TransferCreateRequest(
        from_account_id="acc-001",
        to_account_id="acc-999",
        amount=1000,
    )

    with pytest.raises(HTTPException) as error:
        create_transfer(request)

    assert error.value.status_code == 404
    assert error.value.detail == "Destination account not found"


def test_create_transfer_service_rejects_transfer_to_same_account() -> None:
    request = TransferCreateRequest(
        from_account_id="acc-001",
        to_account_id="acc-001",
        amount=1000,
    )

    with pytest.raises(HTTPException) as error:
        create_transfer(request)

    assert error.value.status_code == 400
    assert error.value.detail == "Cannot transfer to same account"


def test_create_transfer_service_rejects_insufficient_funds() -> None:
    request = TransferCreateRequest(
        from_account_id="acc-001",
        to_account_id="acc-002",
        amount=999999999,
    )

    with pytest.raises(HTTPException) as error:
        create_transfer(request)

    assert error.value.status_code == 400
    assert error.value.detail == "Insufficient funds"
