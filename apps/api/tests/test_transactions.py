from uuid import uuid4

import pytest

pytestmark = pytest.mark.db


def assert_transaction_id_format(transaction_id: str) -> None:
    assert transaction_id.startswith("tx-")
    assert len(transaction_id) > len("tx-")


def create_test_transfer(auth_client) -> str:
    response = auth_client.post(
        "/transfers",
        headers={"Idempotency-Key": str(uuid4())},
        json={
            "from_account_id": "acc-001",
            "to_account_id": "acc-002",
            "amount": 1000,
        },
    )

    assert response.status_code == 201

    transaction_id = response.json()["transaction_id"]
    assert_transaction_id_format(transaction_id)

    return transaction_id


def test_list_transactions_returns_empty_list_by_default(auth_client) -> None:
    response = auth_client.get("/transactions")

    assert response.status_code == 200
    assert response.json() == []


def test_list_transactions_returns_created_transfer_transaction(auth_client) -> None:
    transaction_id = create_test_transfer(auth_client)

    response = auth_client.get("/transactions")

    assert response.status_code == 200

    transactions = response.json()

    assert len(transactions) == 1
    assert transactions[0]["id"] == transaction_id
    assert transactions[0]["from_account_id"] == "acc-001"
    assert transactions[0]["to_account_id"] == "acc-002"
    assert transactions[0]["amount"] == 1000
    assert transactions[0]["currency"] == "RUB"
    assert transactions[0]["status"] == "completed"
    assert transactions[0]["created_at"] is not None


def test_get_transaction_returns_transaction_by_id(auth_client) -> None:
    transaction_id = create_test_transfer(auth_client)

    response = auth_client.get(f"/transactions/{transaction_id}")

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["id"] == transaction_id
    assert response_data["from_account_id"] == "acc-001"
    assert response_data["to_account_id"] == "acc-002"
    assert response_data["amount"] == 1000
    assert response_data["currency"] == "RUB"
    assert response_data["status"] == "completed"
    assert response_data["created_at"] is not None


def test_get_transaction_returns_404_for_unknown_transaction(auth_client) -> None:
    response = auth_client.get("/transactions/tx-unknown")

    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "code": "transaction_not_found",
            "message": "Transaction not found",
        }
    }


def test_list_transactions_filters_by_account_id(auth_client) -> None:
    transaction_id = create_test_transfer(auth_client)

    response = auth_client.get("/transactions?account_id=acc-001")

    assert response.status_code == 200

    transactions = response.json()

    assert len(transactions) == 1
    assert transactions[0]["id"] == transaction_id
    assert transactions[0]["from_account_id"] == "acc-001"
    assert transactions[0]["to_account_id"] == "acc-002"


def test_list_transactions_strips_account_id_filter_spaces(auth_client) -> None:
    transaction_id = create_test_transfer(auth_client)

    response = auth_client.get("/transactions?account_id=%20acc-001%20")

    assert response.status_code == 200

    transactions = response.json()

    assert len(transactions) == 1
    assert transactions[0]["id"] == transaction_id
    assert transactions[0]["from_account_id"] == "acc-001"
    assert transactions[0]["to_account_id"] == "acc-002"


def test_list_transactions_returns_empty_list_for_unknown_account(auth_client) -> None:
    create_test_transfer(auth_client)

    response = auth_client.get("/transactions?account_id=acc-999")

    assert response.status_code == 200
    assert response.json() == []


def test_get_transaction_returns_404_for_blank_transaction_id(auth_client) -> None:
    response = auth_client.get("/transactions/%20%20%20")

    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "code": "transaction_not_found",
            "message": "Transaction not found",
        }
    }


def test_list_transactions_returns_newest_first(auth_client) -> None:
    first_transaction_id = create_test_transfer(auth_client)
    second_transaction_id = create_test_transfer(auth_client)

    response = auth_client.get("/transactions")

    assert response.status_code == 200

    transactions = response.json()

    assert len(transactions) == 2
    assert transactions[0]["id"] == second_transaction_id
    assert transactions[1]["id"] == first_transaction_id


def test_list_transactions_by_account_id_returns_newest_first(auth_client) -> None:
    first_transaction_id = create_test_transfer(auth_client)
    second_transaction_id = create_test_transfer(auth_client)

    response = auth_client.get("/transactions?account_id=acc-001")

    assert response.status_code == 200

    transactions = response.json()

    assert len(transactions) == 2
    assert transactions[0]["id"] == second_transaction_id
    assert transactions[1]["id"] == first_transaction_id


def test_transaction_is_visible_to_destination_owner(auth_client, maria_auth_client) -> None:
    transaction_id = create_test_transfer(auth_client)

    response = maria_auth_client.get(f"/transactions/{transaction_id}")

    assert response.status_code == 200
    assert response.json()["id"] == transaction_id


def test_filter_hides_another_users_account(auth_client) -> None:
    create_test_transfer(auth_client)

    response = auth_client.get("/transactions?account_id=acc-002")

    assert response.status_code == 200
    assert response.json() == []


def test_transactions_require_authentication(client) -> None:
    response = client.get("/transactions")

    assert response.status_code == 401
