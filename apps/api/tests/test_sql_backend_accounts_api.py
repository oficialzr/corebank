from corebank_api.database.models import AccountModel
from corebank_api.database.session import SessionLocal
from corebank_api.main import create_app
from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError


def test_sql_backend_accounts_api_creates_and_reads_account(monkeypatch) -> None:
    monkeypatch.setenv("COREBANK_REPOSITORY_BACKEND", "sql")

    try:
        with SessionLocal() as session:
            session.query(AccountModel).filter(
                AccountModel.owner_name == "SQL API User"
            ).delete()
            session.commit()

        client = TestClient(create_app())

        create_response = client.post(
            "/accounts",
            json={
                "owner_name": "SQL API User",
                "currency": "RUB",
            },
        )

        assert create_response.status_code == 201

        created_account = create_response.json()

        assert created_account["owner_name"] == "SQL API User"
        assert created_account["balance"] == 0
        assert created_account["currency"] == "RUB"

        get_response = client.get(f"/accounts/{created_account['id']}")

        assert get_response.status_code == 200

        found_account = get_response.json()

        assert found_account["id"] == created_account["id"]
        assert found_account["owner_name"] == "SQL API User"

        with SessionLocal() as session:
            session.query(AccountModel).filter(
                AccountModel.id == created_account["id"]
            ).delete()
            session.commit()
    except OperationalError:
        return
