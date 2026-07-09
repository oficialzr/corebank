from corebank_api.database.session import SessionLocal
from corebank_api.repositories import sql_transactions as sql_transactions_repository
from corebank_api.schemas.transaction import TransactionResponse


def get_all_transactions() -> list[TransactionResponse]:
    with SessionLocal() as session:
        return sql_transactions_repository.get_all_transactions(session)


def get_transaction_by_id(transaction_id: str) -> TransactionResponse | None:
    with SessionLocal() as session:
        return sql_transactions_repository.get_transaction_by_id(session, transaction_id)


def get_transactions_by_account_id(account_id: str) -> list[TransactionResponse]:
    with SessionLocal() as session:
        return sql_transactions_repository.get_transactions_by_account_id(
            session,
            account_id,
        )


def save_transaction(transaction: TransactionResponse) -> TransactionResponse:
    with SessionLocal() as session:
        return sql_transactions_repository.save_transaction(session, transaction)


def generate_transaction_id() -> str:
    with SessionLocal() as session:
        return sql_transactions_repository.generate_transaction_id(session)
