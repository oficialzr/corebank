from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from corebank_api.database.models import AccountModel, TransactionModel
from corebank_api.schemas.transaction import TransactionResponse


def mask_card_number(card_number: str | None) -> str | None:
    return f"•••• {card_number[-4:]}" if card_number else None


def model_to_schema(transaction: TransactionModel, session: Session | None = None) -> TransactionResponse:
    account_cards: dict[str, str] = {}
    if session is not None:
        account_cards = dict(
            session.query(AccountModel.id, AccountModel.card_number)
            .filter(AccountModel.id.in_([transaction.from_account_id, transaction.to_account_id]))
            .all()
        )
    return TransactionResponse(
        id=transaction.id,
        from_account_id=transaction.from_account_id,
        to_account_id=transaction.to_account_id,
        from_account=mask_card_number(account_cards.get(transaction.from_account_id)),
        to_account=mask_card_number(account_cards.get(transaction.to_account_id)),
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
    limit: int | None = None,
    offset: int = 0,
) -> list[TransactionResponse]:
    owned_account_ids = select(AccountModel.id).where(AccountModel.user_id == user_id)
    query = (
        session.query(TransactionModel)
        .filter(
            or_(
                TransactionModel.from_account_id.in_(owned_account_ids),
                TransactionModel.to_account_id.in_(owned_account_ids),
            )
        )
        .order_by(TransactionModel.created_at.desc())
    )
    if limit is not None:
        query = query.limit(limit).offset(offset)
    transactions = query.all()
    return [model_to_schema(transaction, session) for transaction in transactions]


def get_transaction_by_id(
    session: Session,
    transaction_id: str,
) -> TransactionResponse | None:
    transaction = session.get(TransactionModel, transaction_id)

    if transaction is None:
        return None

    return model_to_schema(transaction, session)


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
    limit: int | None = None,
    offset: int = 0,
) -> list[TransactionResponse]:
    account_exists = (
        session.query(AccountModel.id)
        .filter(AccountModel.id == account_id, AccountModel.user_id == user_id)
        .first()
    )

    if account_exists is None:
        return []

    query = (
        session.query(TransactionModel)
        .filter(
            (TransactionModel.from_account_id == account_id)
            | (TransactionModel.to_account_id == account_id)
        )
        .order_by(TransactionModel.created_at.desc())
    )
    if limit is not None:
        query = query.limit(limit).offset(offset)
    return [model_to_schema(transaction, session) for transaction in query.all()]


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
