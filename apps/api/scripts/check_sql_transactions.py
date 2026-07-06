from datetime import UTC, datetime

from corebank_api.database.session import SessionLocal
from corebank_api.repositories.sql_transactions import (
    generate_transaction_id,
    get_all_transactions,
    get_transaction_by_id,
    get_transactions_by_account_id,
    save_transaction,
)
from corebank_api.schemas.common import Currency
from corebank_api.schemas.transaction import TransactionResponse
from corebank_api.schemas.transfer import TransferStatus


def main() -> None:
    with SessionLocal() as session:
        transaction_id = generate_transaction_id(session)

        transaction = TransactionResponse(
            id=transaction_id,
            from_account_id="acc-sql-001",
            to_account_id="acc-sql-002",
            amount=1000,
            currency=Currency.RUB,
            status=TransferStatus.COMPLETED,
            created_at=datetime.now(UTC),
        )

        save_transaction(session, transaction)

        print(get_transaction_by_id(session, transaction_id))
        print(get_transactions_by_account_id(session, "acc-sql-001"))
        print(get_all_transactions(session))


if __name__ == "__main__":
    main()
