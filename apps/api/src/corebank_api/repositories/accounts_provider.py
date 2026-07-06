from corebank_api.core.config import get_settings
from corebank_api.repositories import accounts as memory_accounts_repository
from corebank_api.repositories import sql_accounts as sql_accounts_repository


def get_accounts_repository():
    settings = get_settings()

    if settings.repository_backend == "sql":
        return sql_accounts_repository

    return memory_accounts_repository
