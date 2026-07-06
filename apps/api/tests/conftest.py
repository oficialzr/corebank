import pytest

from corebank_api.repositories.accounts import reset_accounts_repository


@pytest.fixture(autouse=True)
def reset_repository_between_tests() -> None:
    reset_accounts_repository()