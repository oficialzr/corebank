from corebank_api.repositories.transactions import (
    get_all_transactions,
    get_transaction_by_id,
)
from corebank_api.schemas.transaction import TransactionResponse


def list_transactions() -> list[TransactionResponse]:
    return get_all_transactions()


def get_transaction(transaction_id: str) -> TransactionResponse | None:
    return get_transaction_by_id(transaction_id)
