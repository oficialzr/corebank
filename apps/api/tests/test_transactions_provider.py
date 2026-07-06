from corebank_api.repositories import sql_transactions as sql_transactions_repository
from corebank_api.repositories import transactions as memory_transactions_repository
from corebank_api.repositories.transactions_provider import (
    get_transactions_repository,
)


def test_get_transactions_repository_returns_memory_by_default(monkeypatch) -> None:
    monkeypatch.delenv("COREBANK_REPOSITORY_BACKEND", raising=False)

    repository = get_transactions_repository()

    assert repository is memory_transactions_repository


def test_get_transactions_repository_returns_sql_from_env(monkeypatch) -> None:
    monkeypatch.setenv("COREBANK_REPOSITORY_BACKEND", "sql")

    repository = get_transactions_repository()

    assert repository is sql_transactions_repository
