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
    assert response.json() == [
        {
            "id": "tx-001",
            "from_account_id": "acc-001",
            "to_account_id": "acc-002",
            "amount": 1000,
            "currency": "RUB",
            "status": "completed",
        },
    ]


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


def test_get_transaction_returns_404_for_unknown_transaction(client) -> None:
    response = client.get("/transactions/tx-999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Transaction not found",
    }
