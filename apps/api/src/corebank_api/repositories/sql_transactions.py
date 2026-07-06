from datetime import UTC, datetime

from sqlalchemy.orm import Session

from corebank_api.database.models import TransactionModel
from corebank_api.schemas.transaction import TransactionResponse


def model_to_schema(transaction: TransactionModel) -> TransactionResponse:
    return TransactionResponse(
        id=transaction.id,
        from_account_id=transaction.from_account_id,
        to_account_id=transaction.to_account_id,
        amount=transaction.amount,
        currency=transaction.currency,
        status=transaction.status,
        created_at=transaction.created_at,
    )


def get_all_transactions(session: Session) -> list[TransactionResponse]:
    transactions = session.query(TransactionModel).order_by(TransactionModel.id).all()
    return [model_to_schema(transaction) for transaction in transactions]


def get_transaction_by_id(
    session: Session,
    transaction_id: str,
) -> TransactionResponse | None:
    transaction = session.get(TransactionModel, transaction_id)

    if transaction is None:
        return None

    return model_to_schema(transaction)


def get_transactions_by_account_id(
    session: Session,
    account_id: str,
) -> list[TransactionResponse]:
    transactions = (
        session.query(TransactionModel)
        .filter(
            (TransactionModel.from_account_id == account_id)
            | (TransactionModel.to_account_id == account_id),
        )
        .order_by(TransactionModel.id)
        .all()
    )

    return [model_to_schema(transaction) for transaction in transactions]


def save_transaction(
    session: Session,
    transaction: TransactionResponse,
    *,
    commit: bool = True,
) -> TransactionResponse:
    transaction_model = TransactionModel(
        id=transaction.id,
        from_account_id=transaction.from_account_id,
        to_account_id=transaction.to_account_id,
        amount=transaction.amount,
        currency=str(transaction.currency),
        status=str(transaction.status),
        created_at=getattr(transaction, "created_at", datetime.now(UTC)),
    )

    session.add(transaction_model)

    if commit:
        session.commit()
        session.refresh(transaction_model)

    return model_to_schema(transaction_model)


def generate_transaction_id(session: Session) -> str:
    transactions_count = session.query(TransactionModel).count()
    next_number = transactions_count + 1

    return f"tx-{next_number:03}"
