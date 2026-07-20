from corebank_api.repositories import transactions_provider as transactions_repository
from corebank_api.schemas.transaction import TransactionResponse


def list_transactions(user_id: str) -> list[TransactionResponse]:
    return transactions_repository.get_transactions_by_user_id(user_id)


def get_transaction(transaction_id: str, user_id: str) -> TransactionResponse | None:
    return transactions_repository.get_transaction_by_id_and_user_id(transaction_id, user_id)


def list_transactions_by_account_id(account_id: str, user_id: str) -> list[TransactionResponse]:
    return transactions_repository.get_transactions_by_account_id_and_user_id(account_id, user_id)
