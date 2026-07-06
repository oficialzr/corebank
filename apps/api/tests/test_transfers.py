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
    assert response.json() == {
        "transaction_id": "tx-001",
        "from_account_id": "acc-001",
        "to_account_id": "acc-002",
        "amount": 1000,
        "status": "completed",
    }

    from_account_response = client.get("/accounts/acc-001")
    to_account_response = client.get("/accounts/acc-002")

    assert from_account_response.json()["balance"] == 99000
    assert to_account_response.json()["balance"] == 251000


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
        "detail": "Source account not found",
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
        "detail": "Destination account not found",
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
        "detail": "Cannot transfer to same account",
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
        "detail": "Insufficient funds",
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
        "detail": "Currency mismatch",
    }
