from datetime import UTC, datetime

import pytest
from corebank_api.core.security import create_access_token
from corebank_api.database.models import (
    AccountModel,
    TransactionModel,
    UserModel,
)
from corebank_api.database.session import SessionLocal
from corebank_api.main import create_app
from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError


def reset_postgres_test_data() -> None:
    with SessionLocal() as session:
        session.query(TransactionModel).delete(synchronize_session=False)
        session.query(AccountModel).delete(synchronize_session=False)
        session.query(UserModel).delete(synchronize_session=False)

        session.add_all(
            [
                UserModel(
                    id="user-alex",
                    email="owner-alex@example.com",
                    password_hash="not-used-in-seeded-tests",
                    full_name="Alex Ivanov",
                    is_active=True,
                    created_at=datetime.now(UTC),
                ),
                UserModel(
                    id="user-maria",
                    email="owner-maria@example.com",
                    password_hash="not-used-in-seeded-tests",
                    full_name="Maria Petrova",
                    is_active=True,
                    created_at=datetime.now(UTC),
                ),
            ]
        )
        session.flush()

        session.add_all(
            [
                AccountModel(
                    id="acc-001",
                    user_id="user-alex",
                    owner_name="Alex Ivanov",
                    balance=100000,
                    currency="RUB",
                    created_at=datetime.now(UTC),
                ),
                AccountModel(
                    id="acc-002",
                    user_id="user-maria",
                    owner_name="Maria Petrova",
                    balance=50000,
                    currency="RUB",
                    created_at=datetime.now(UTC),
                ),
            ]
        )

        session.commit()


@pytest.fixture(autouse=True)
def reset_repository_between_tests(request) -> None:
    if "db" not in request.keywords:
        return

    try:
        reset_postgres_test_data()
    except OperationalError:
        pytest.skip("PostgreSQL is not available")


@pytest.fixture
def client() -> TestClient:
    app = create_app()
    return TestClient(app)


@pytest.fixture
def auth_client() -> TestClient:
    app = create_app()
    token = create_access_token("owner-alex@example.com")
    return TestClient(app, headers={"Authorization": f"Bearer {token}"})


@pytest.fixture
def maria_auth_client() -> TestClient:
    app = create_app()
    token = create_access_token("owner-maria@example.com")
    return TestClient(app, headers={"Authorization": f"Bearer {token}"})
