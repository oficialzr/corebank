from corebank_api.schemas.transaction import TransactionResponse

TRANSACTIONS: list[TransactionResponse] = []


def reset_transactions_repository() -> None:
    TRANSACTIONS.clear()


def generate_transaction_id() -> str:
    next_number = len(TRANSACTIONS) + 1
    return f"tx-{next_number:03d}"


def get_all_transactions() -> list[TransactionResponse]:
    return TRANSACTIONS


def get_transaction_by_id(transaction_id: str) -> TransactionResponse | None:
    for transaction in TRANSACTIONS:
        if transaction.id == transaction_id:
            return transaction

    return None


def save_transaction(transaction: TransactionResponse) -> TransactionResponse:
    TRANSACTIONS.append(transaction)
    return transaction
