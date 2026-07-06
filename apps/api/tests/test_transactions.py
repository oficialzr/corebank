def test_list_transactions_returns_empty_list(client) -> None:
    response = client.get("/transactions")

    assert response.status_code == 200
    assert response.json() == []


def test_list_transactions_returns_created_transfer_transaction(client) -> None:
    client.post(
        "/transfers",
        json={
            "from_account_id": "acc-001",
            "to_account_id": "acc-002",
            "amount": 1000,
        },
    )

    response = client.get("/transactions")

    assert response.status_code == 200

    transactions = response.json()

    assert len(transactions) == 1
    assert transactions[0]["id"] == "tx-001"
    assert transactions[0]["from_account_id"] == "acc-001"
    assert transactions[0]["to_account_id"] == "acc-002"
    assert transactions[0]["amount"] == 1000
    assert transactions[0]["currency"] == "RUB"
    assert transactions[0]["status"] == "completed"
    assert "created_at" in transactions[0]


def test_get_transaction_returns_transaction_by_id(client) -> None:
    client.post(
        "/transfers",
        json={
            "from_account_id": "acc-001",
            "to_account_id": "acc-002",
            "amount": 1000,
        },
    )

    response = client.get("/transactions/tx-001")

    assert response.status_code == 200
    assert response.json()["id"] == "tx-001"
    assert response.json()["amount"] == 1000
    assert "created_at" in response.json()


def test_get_transaction_returns_404_for_unknown_transaction(client) -> None:
    response = client.get("/transactions/tx-999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Transaction not found",
    }


def test_list_transactions_filters_by_account_id(client) -> None:
    client.post(
        "/transfers",
        json={
            "from_account_id": "acc-001",
            "to_account_id": "acc-002",
            "amount": 1000,
        },
    )

    response = client.get("/transactions?account_id=acc-001")

    assert response.status_code == 200

    transactions = response.json()

    assert len(transactions) == 1
    assert transactions[0]["id"] == "tx-001"
    assert transactions[0]["from_account_id"] == "acc-001"
    assert transactions[0]["to_account_id"] == "acc-002"


def test_list_transactions_filters_by_account_id_returns_empty_list(client) -> None:
    client.post(
        "/transfers",
        json={
            "from_account_id": "acc-001",
            "to_account_id": "acc-002",
            "amount": 1000,
        },
    )

    response = client.get("/transactions?account_id=acc-999")

    assert response.status_code == 200
    assert response.json() == []


def test_list_transactions_rejects_empty_account_id_filter(client) -> None:
    response = client.get("/transactions?account_id=")

    assert response.status_code == 422


def test_list_transactions_rejects_blank_account_id_filter(client) -> None:
    response = client.get("/transactions?account_id=+++")

    assert response.status_code == 422
    assert response.json() == {
        "detail": "account_id must not be blank",
    }


def test_list_transactions_strips_account_id_filter_spaces(client) -> None:
    client.post(
        "/transfers",
        json={
            "from_account_id": "acc-001",
            "to_account_id": "acc-002",
            "amount": 1000,
        },
    )

    response = client.get("/transactions?account_id=+acc-001+")

    assert response.status_code == 200

    transactions = response.json()

    assert len(transactions) == 1
    assert transactions[0]["id"] == "tx-001"
