import pytest

pytestmark = pytest.mark.db


def assert_transaction_id_format(transaction_id: str) -> None:
    assert transaction_id.startswith("tx-")
    assert len(transaction_id) > len("tx-")


def test_create_transfer_moves_money_between_accounts(client) -> None:
    response = client.post(
        "/transfers",
        json={
            "from_account_id": "acc-001",
            "to_account_id": "acc-002",
            "amount": 1000,
        },
    )

    assert response.status_code == 201
    response_data = response.json()

    assert_transaction_id_format(response_data["transaction_id"])
    assert response_data["from_account_id"] == "acc-001"
    assert response_data["to_account_id"] == "acc-002"
    assert response_data["amount"] == 1000
    assert response_data["status"] == "completed"

    from_account_response = client.get("/accounts/acc-001")
    to_account_response = client.get("/accounts/acc-002")

    assert from_account_response.json()["balance"] == 99000
    assert to_account_response.json()["balance"] == 51000


def test_create_transfer_returns_404_for_unknown_source_account(client) -> None:
    response = client.post(
        "/transfers",
        json={
            "from_account_id": "acc-999",
            "to_account_id": "acc-002",
            "amount": 1000,
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "code": "source_account_not_found",
            "message": "Source account not found",
        }
    }


def test_create_transfer_returns_404_for_unknown_destination_account(client) -> None:
    response = client.post(
        "/transfers",
        json={
            "from_account_id": "acc-001",
            "to_account_id": "acc-999",
            "amount": 1000,
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "code": "destination_account_not_found",
            "message": "Destination account not found",
        }
    }


def test_create_transfer_rejects_transfer_to_same_account(client) -> None:
    response = client.post(
        "/transfers",
        json={
            "from_account_id": "acc-001",
            "to_account_id": "acc-001",
            "amount": 1000,
        },
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": {
            "code": "same_account_transfer",
            "message": "Cannot transfer to same account",
        }
    }


def test_create_transfer_rejects_insufficient_funds(client) -> None:
    response = client.post(
        "/transfers",
        json={
            "from_account_id": "acc-001",
            "to_account_id": "acc-002",
            "amount": 999999999,
        },
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": {
            "code": "insufficient_funds",
            "message": "Insufficient funds",
        }
    }


def test_create_transfer_rejects_zero_amount(client) -> None:
    response = client.post(
        "/transfers",
        json={
            "from_account_id": "acc-001",
            "to_account_id": "acc-002",
            "amount": 0,
        },
    )

    assert response.status_code == 422


def test_create_transfer_rejects_negative_amount(client) -> None:
    response = client.post(
        "/transfers",
        json={
            "from_account_id": "acc-001",
            "to_account_id": "acc-002",
            "amount": -100,
        },
    )

    assert response.status_code == 422


def test_create_transfer_rejects_currency_mismatch(client) -> None:
    create_account_response = client.post(
        "/accounts",
        json={
            "owner_name": "Usd User",
            "currency": "USD",
        },
    )

    usd_account_id = create_account_response.json()["id"]

    response = client.post(
        "/transfers",
        json={
            "from_account_id": "acc-001",
            "to_account_id": usd_account_id,
            "amount": 1000,
        },
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": {
            "code": "currency_mismatch",
            "message": "Currency mismatch",
        }
    }


def test_create_transfer_returns_next_transaction_id(client) -> None:
    first_response = client.post(
        "/transfers",
        json={
            "from_account_id": "acc-001",
            "to_account_id": "acc-002",
            "amount": 1000,
        },
    )

    second_response = client.post(
        "/transfers",
        json={
            "from_account_id": "acc-001",
            "to_account_id": "acc-002",
            "amount": 1000,
        },
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 201

    first_transaction_id = first_response.json()["transaction_id"]
    second_transaction_id = second_response.json()["transaction_id"]

    assert_transaction_id_format(first_transaction_id)
    assert_transaction_id_format(second_transaction_id)

    assert first_transaction_id != second_transaction_id
