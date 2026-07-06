def test_list_accounts_returns_accounts(client) -> None:
    response = client.get("/accounts")

    assert response.status_code == 200

    accounts = response.json()

    assert len(accounts) >= 2
    assert accounts[0]["id"] == "acc-001"
    assert accounts[0]["owner_name"] == "Alex Ivanov"
    assert accounts[0]["balance"] == 100000
    assert accounts[0]["currency"] == "RUB"


def test_get_account_returns_account_by_id(client) -> None:
    response = client.get("/accounts/acc-001")

    assert response.status_code == 200
    assert response.json() == {
        "id": "acc-001",
        "owner_name": "Alex Ivanov",
        "balance": 100000,
        "currency": "RUB",
    }


def test_get_account_returns_404_for_unknown_account(client) -> None:
    response = client.get("/accounts/acc-999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Account not found",
    }


def test_create_account_returns_created_account(client) -> None:
    response = client.post(
        "/accounts",
        json={
            "owner_name": "Ivan Sidorov",
            "currency": "RUB",
        },
    )

    assert response.status_code == 201

    account = response.json()

    assert account["id"].startswith("acc-")
    assert account["owner_name"] == "Ivan Sidorov"
    assert account["balance"] == 0
    assert account["currency"] == "RUB"


def test_create_account_rejects_empty_owner_name(client) -> None:
    response = client.post(
        "/accounts",
        json={"owner_name": "", "currency": "RUB"},
    )

    assert response.status_code == 422


def test_create_account_rejects_unknown_currency(client) -> None:
    response = client.post(
        "/accounts",
        json={"owner_name": "Ivan Sidorov", "currency": "GBP"},
    )

    assert response.status_code == 422
