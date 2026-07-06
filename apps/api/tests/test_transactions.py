def assert_transaction_id_format(transaction_id: str) -> None:
    assert transaction_id.startswith("tx-")
    assert len(transaction_id) > len("tx-")


def create_test_transfer(client) -> str:
    response = client.post(
        "/transfers",
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


def test_list_transactions_returns_empty_list_by_default(client) -> None:
    response = client.get("/transactions")

    assert response.status_code == 200
    assert response.json() == []


def test_list_transactions_returns_created_transfer_transaction(client) -> None:
    transaction_id = create_test_transfer(client)

    response = client.get("/transactions")

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


def test_get_transaction_returns_transaction_by_id(client) -> None:
    transaction_id = create_test_transfer(client)

    response = client.get(f"/transactions/{transaction_id}")

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["id"] == transaction_id
    assert response_data["from_account_id"] == "acc-001"
    assert response_data["to_account_id"] == "acc-002"
    assert response_data["amount"] == 1000
    assert response_data["currency"] == "RUB"
    assert response_data["status"] == "completed"
    assert response_data["created_at"] is not None


def test_get_transaction_returns_404_for_unknown_transaction(client) -> None:
    response = client.get("/transactions/tx-unknown")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Transaction not found",
    }


def test_list_transactions_filters_by_account_id(client) -> None:
    transaction_id = create_test_transfer(client)

    response = client.get("/transactions?account_id=acc-001")

    assert response.status_code == 200

    transactions = response.json()

    assert len(transactions) == 1
    assert transactions[0]["id"] == transaction_id
    assert transactions[0]["from_account_id"] == "acc-001"
    assert transactions[0]["to_account_id"] == "acc-002"


def test_list_transactions_strips_account_id_filter_spaces(client) -> None:
    transaction_id = create_test_transfer(client)

    response = client.get("/transactions?account_id=%20acc-001%20")

    assert response.status_code == 200

    transactions = response.json()

    assert len(transactions) == 1
    assert transactions[0]["id"] == transaction_id
    assert transactions[0]["from_account_id"] == "acc-001"
    assert transactions[0]["to_account_id"] == "acc-002"


def test_list_transactions_returns_empty_list_for_unknown_account(client) -> None:
    create_test_transfer(client)

    response = client.get("/transactions?account_id=acc-999")

    assert response.status_code == 200
    assert response.json() == []


def test_get_transaction_returns_404_for_blank_transaction_id(client) -> None:
    response = client.get("/transactions/%20%20%20")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Transaction not found",
    }
