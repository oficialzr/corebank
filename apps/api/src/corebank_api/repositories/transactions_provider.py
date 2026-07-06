from corebank_api.core.config import get_settings
from corebank_api.database.session import SessionLocal
from corebank_api.repositories import sql_transactions as sql_transactions_repository
from corebank_api.repositories import transactions as memory_transactions_repository
from corebank_api.schemas.transaction import TransactionResponse


def use_sql_backend() -> bool:
    return get_settings().repository_backend == "sql"


def get_all_transactions() -> list[TransactionResponse]:
    if use_sql_backend():
        with SessionLocal() as session:
            return sql_transactions_repository.get_all_transactions(session)

    return memory_transactions_repository.get_all_transactions()


def get_transaction_by_id(transaction_id: str) -> TransactionResponse | None:
    if use_sql_backend():
        with SessionLocal() as session:
            return sql_transactions_repository.get_transaction_by_id(
                session,
                transaction_id,
            )

    return memory_transactions_repository.get_transaction_by_id(transaction_id)


def get_transactions_by_account_id(account_id: str) -> list[TransactionResponse]:
    if use_sql_backend():
        with SessionLocal() as session:
            return sql_transactions_repository.get_transactions_by_account_id(
                session,
                account_id,
            )

    return memory_transactions_repository.get_transactions_by_account_id(account_id)


def save_transaction(transaction: TransactionResponse) -> TransactionResponse:
    if use_sql_backend():
        with SessionLocal() as session:
            return sql_transactions_repository.save_transaction(session, transaction)

    return memory_transactions_repository.save_transaction(transaction)


def generate_transaction_id() -> str:
    if use_sql_backend():
        with SessionLocal() as session:
            return sql_transactions_repository.generate_transaction_id(session)

    return memory_transactions_repository.generate_transaction_id()