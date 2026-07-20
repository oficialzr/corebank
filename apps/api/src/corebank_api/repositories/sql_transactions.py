from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from corebank_api.database.models import AccountModel, TransactionModel
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
    transactions = session.query(TransactionModel).order_by(TransactionModel.created_at.desc()).all()
    return [model_to_schema(transaction) for transaction in transactions]


def get_transactions_by_user_id(
    session: Session,
    user_id: str,
) -> list[TransactionResponse]:
    owned_account_ids = select(AccountModel.id).where(AccountModel.user_id == user_id)
    transactions = (
        session.query(TransactionModel)
        .filter(
            or_(
                TransactionModel.from_account_id.in_(owned_account_ids),
                TransactionModel.to_account_id.in_(owned_account_ids),
            )
        )
        .order_by(TransactionModel.created_at.desc())
        .all()
    )
    return [model_to_schema(transaction) for transaction in transactions]


def get_transaction_by_id(
    session: Session,
    transaction_id: str,
) -> TransactionResponse | None:
    transaction = session.get(TransactionModel, transaction_id)

    if transaction is None:
        return None

    return model_to_schema(transaction)


def get_transaction_by_id_and_user_id(
    session: Session,
    transaction_id: str,
    user_id: str,
) -> TransactionResponse | None:
    owned_account_ids = select(AccountModel.id).where(AccountModel.user_id == user_id)
    transaction = (
        session.query(TransactionModel)
        .filter(
            TransactionModel.id == transaction_id,
            or_(
                TransactionModel.from_account_id.in_(owned_account_ids),
                TransactionModel.to_account_id.in_(owned_account_ids),
            ),
        )
        .one_or_none()
    )

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
            (TransactionModel.from_account_id == account_id) | (TransactionModel.to_account_id == account_id),
        )
        .order_by(TransactionModel.created_at.desc())
        .all()
    )

    return [model_to_schema(transaction) for transaction in transactions]


def get_transactions_by_account_id_and_user_id(
    session: Session,
    account_id: str,
    user_id: str,
) -> list[TransactionResponse]:
    account_exists = (
        session.query(AccountModel.id)
        .filter(AccountModel.id == account_id, AccountModel.user_id == user_id)
        .first()
    )

    if account_exists is None:
        return []

    return get_transactions_by_account_id(session, account_id)


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
    return f"tx-{uuid4()}"
