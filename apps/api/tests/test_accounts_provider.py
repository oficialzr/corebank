from corebank_api.repositories import accounts as memory_accounts_repository
from corebank_api.repositories import sql_accounts as sql_accounts_repository
from corebank_api.repositories.accounts_provider import get_accounts_repository


def test_get_accounts_repository_returns_memory_by_default(monkeypatch) -> None:
    monkeypatch.delenv("COREBANK_REPOSITORY_BACKEND", raising=False)

    repository = get_accounts_repository()

    assert repository is memory_accounts_repository


def test_get_accounts_repository_returns_sql_from_env(monkeypatch) -> None:
    monkeypatch.setenv("COREBANK_REPOSITORY_BACKEND", "sql")

    repository = get_accounts_repository()

    assert repository is sql_accounts_repository
