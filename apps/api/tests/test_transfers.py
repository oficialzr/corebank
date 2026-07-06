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
        "from_account_id": "acc-001",
        "to_account_id": "acc-002",
        "amount": 1000,
        "status": "completed",
    }

    from_account_response = client.get("/accounts/acc-001")
    to_account_response = client.get("/accounts/acc-002")

    assert from_account_response.json()["balance"] == 99000
    assert to_account_response.json()["balance"] == 251000
