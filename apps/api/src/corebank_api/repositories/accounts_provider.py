from corebank_api.core.config import get_settings
from corebank_api.database.session import SessionLocal
from corebank_api.repositories import accounts as memory_accounts_repository
from corebank_api.repositories import sql_accounts as sql_accounts_repository
from corebank_api.schemas.account import AccountResponse


def use_sql_backend() -> bool:
    return get_settings().repository_backend == "sql"


def get_all_accounts() -> list[AccountResponse]:
    if use_sql_backend():
        with SessionLocal() as session:
            return sql_accounts_repository.get_all_accounts(session)

    return memory_accounts_repository.get_all_accounts()


def get_account_by_id(account_id: str) -> AccountResponse | None:
    if use_sql_backend():
        with SessionLocal() as session:
            return sql_accounts_repository.get_account_by_id(session, account_id)

    return memory_accounts_repository.get_account_by_id(account_id)


def save_account(account: AccountResponse) -> AccountResponse:
    if use_sql_backend():
        with SessionLocal() as session:
            return sql_accounts_repository.save_account(session, account)

    return memory_accounts_repository.save_account(account)


def update_account_balance(account_id: str, balance: int) -> None:
    if use_sql_backend():
        with SessionLocal() as session:
            sql_accounts_repository.update_account_balance(session, account_id, balance)
            return

    memory_accounts_repository.update_account_balance(account_id, balance)