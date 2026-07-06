import pytest
from corebank_api.main import create_app
from corebank_api.repositories.accounts import reset_accounts_repository
from corebank_api.repositories.transactions import reset_transactions_repository
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def reset_repository_between_tests() -> None:
    reset_accounts_repository()
    reset_transactions_repository()


@pytest.fixture
def client() -> TestClient:
    app = create_app()
    return TestClient(app)
