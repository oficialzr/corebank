from corebank_api.core.config import get_settings
from corebank_api.repositories import transactions as memory_transactions_repository
from corebank_api.repositories import sql_transactions as sql_transactions_repository


def get_transactions_repository():
    settings = get_settings()

    if settings.repository_backend == "sql":
        return sql_transactions_repository

    return memory_transactions_repository
