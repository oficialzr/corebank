from corebank_api.main import create_app
from fastapi.testclient import TestClient


def test_list_accounts_returns_accounts() -> None:
    app = create_app()
    client = TestClient(app)

    response = client.get("/accounts")

    assert response.status_code == 200

    accounts = response.json()

    assert len(accounts) == 2
    assert accounts[0]["id"] == "acc-001"
    assert accounts[0]["owner_name"] == "Alex Ivanov"
    assert accounts[0]["balance"] == 100000
    assert accounts[0]["currency"] == "RUB"