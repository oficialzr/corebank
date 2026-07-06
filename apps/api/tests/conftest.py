from datetime import UTC, datetime

import pytest
from corebank_api.database.models import AccountModel, TransactionModel
from corebank_api.database.session import SessionLocal
from corebank_api.main import create_app
from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError


def reset_postgres_test_data() -> None:
    with SessionLocal() as session:
        session.query(TransactionModel).delete(synchronize_session=False)
        session.query(AccountModel).delete(synchronize_session=False)

        session.add_all(
            [
                AccountModel(
                    id="acc-001",
                    owner_name="Alex Ivanov",
                    balance=100000,
                    currency="RUB",
                    created_at=datetime.now(UTC),
                ),
                AccountModel(
                    id="acc-002",
                    owner_name="Maria Petrova",
                    balance=50000,
                    currency="RUB",
                    created_at=datetime.now(UTC),
                ),
            ]
        )

        session.commit()


@pytest.fixture(autouse=True)
def reset_repository_between_tests() -> None:
    try:
        reset_postgres_test_data()
    except OperationalError:
        pytest.skip("PostgreSQL is not available")


@pytest.fixture
def client() -> TestClient:
    app = create_app()
    return TestClient(app)
