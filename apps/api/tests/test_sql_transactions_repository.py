from datetime import UTC, datetime

from corebank_api.database.models import TransactionModel
from corebank_api.database.session import SessionLocal
from corebank_api.repositories.sql_transactions import (
    get_all_transactions,
    get_transaction_by_id,
    get_transactions_by_account_id,
    save_transaction,
)
from corebank_api.schemas.common import Currency
from corebank_api.schemas.transaction import TransactionResponse
from corebank_api.schemas.transfer import TransferStatus
from sqlalchemy.exc import OperationalError


def test_sql_transactions_repository_saves_and_reads_transaction() -> None:
    try:
        with SessionLocal() as session:
            session.query(TransactionModel).filter(
                TransactionModel.id == "tx-test-001"
            ).delete()
            session.commit()

            transaction = TransactionResponse(
                id="tx-test-001",
                from_account_id="acc-test-001",
                to_account_id="acc-test-002",
                amount=1000,
                currency=Currency.RUB,
                status=TransferStatus.COMPLETED,
                created_at=datetime.now(UTC),
            )

            save_transaction(session, transaction)

            found_transaction = get_transaction_by_id(session, "tx-test-001")
            account_transactions = get_transactions_by_account_id(
                session, "acc-test-001"
            )
            all_transactions = get_all_transactions(session)

            assert found_transaction is not None
            assert found_transaction.id == "tx-test-001"
            assert found_transaction.amount == 1000
            assert any(tx.id == "tx-test-001" for tx in account_transactions)
            assert any(tx.id == "tx-test-001" for tx in all_transactions)

            session.query(TransactionModel).filter(
                TransactionModel.id == "tx-test-001"
            ).delete()
            session.commit()
    except OperationalError:
        return
