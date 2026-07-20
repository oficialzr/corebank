import pytest

pytestmark = pytest.mark.db


def test_list_accounts_returns_accounts(auth_client) -> None:
    response = auth_client.get("/accounts")

    assert response.status_code == 200

    accounts = response.json()

    assert len(accounts) == 1
    assert accounts[0]["id"] == "acc-001"
    assert accounts[0]["user_id"] == "user-alex"
    assert accounts[0]["owner_name"] == "Alex Ivanov"
    assert accounts[0]["balance"] == 100000
    assert accounts[0]["currency"] == "RUB"
    assert accounts[0]["created_at"] is not None


def test_get_account_returns_account_by_id(auth_client) -> None:
    response = auth_client.get("/accounts/acc-001")

    assert response.status_code == 200

    account = response.json()

    assert account["id"] == "acc-001"
    assert account["owner_name"] == "Alex Ivanov"
    assert account["balance"] == 100000
    assert account["currency"] == "RUB"
    assert account["created_at"] is not None


def test_get_account_returns_404_for_unknown_account(auth_client) -> None:
    response = auth_client.get("/accounts/acc-999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": {
            "code": "account_not_found",
            "message": "Account not found",
        }
    }


def test_create_account_returns_created_account(auth_client) -> None:
    response = auth_client.post(
        "/accounts",
        json={"currency": "RUB"},
    )

    assert response.status_code == 201

    account = response.json()

    assert account["id"].startswith("acc-")
    assert account["user_id"] == "user-alex"
    assert account["owner_name"] == "Alex Ivanov"
    assert account["balance"] == 0
    assert account["currency"] == "RUB"
    assert account["created_at"] is not None


def test_create_account_rejects_unknown_currency(auth_client) -> None:
    response = auth_client.post(
        "/accounts",
        json={"currency": "GBP"},
    )

    assert response.status_code == 422


def test_get_account_hides_another_users_account(auth_client) -> None:
    response = auth_client.get("/accounts/acc-002")

    assert response.status_code == 404


def test_list_accounts_isolates_users(auth_client, maria_auth_client) -> None:
    alex_accounts = auth_client.get("/accounts").json()
    maria_accounts = maria_auth_client.get("/accounts").json()

    assert [account["id"] for account in alex_accounts] == ["acc-001"]
    assert [account["id"] for account in maria_accounts] == ["acc-002"]


def test_accounts_require_authentication(client) -> None:
    response = client.get("/accounts")

    assert response.status_code == 401
