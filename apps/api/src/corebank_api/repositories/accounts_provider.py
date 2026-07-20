from corebank_api.database.session import SessionLocal
from corebank_api.repositories import sql_accounts as sql_accounts_repository
from corebank_api.schemas.account import AccountResponse


def get_all_accounts() -> list[AccountResponse]:
    with SessionLocal() as session:
        return sql_accounts_repository.get_all_accounts(session)


def get_accounts_by_user_id(user_id: str) -> list[AccountResponse]:
    with SessionLocal() as session:
        return sql_accounts_repository.get_accounts_by_user_id(session, user_id)


def get_account_by_id(account_id: str) -> AccountResponse | None:
    with SessionLocal() as session:
        return sql_accounts_repository.get_account_by_id(session, account_id)


def get_account_by_id_and_user_id(account_id: str, user_id: str) -> AccountResponse | None:
    with SessionLocal() as session:
        return sql_accounts_repository.get_account_by_id_and_user_id(session, account_id, user_id)


def save_account(account: AccountResponse) -> AccountResponse:
    with SessionLocal() as session:
        return sql_accounts_repository.save_account(session, account)


def update_account_balance(account_id: str, balance: int) -> None:
    with SessionLocal() as session:
        sql_accounts_repository.update_account_balance(session, account_id, balance)
