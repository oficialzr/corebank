from sqlalchemy.orm import Session

from corebank_api.database.models import AccountModel
from corebank_api.schemas.account import AccountResponse


def model_to_schema(account: AccountModel) -> AccountResponse:
    return AccountResponse(
        id=account.id,
        user_id=account.user_id,
        owner_name=account.owner_name,
        balance=account.balance,
        currency=account.currency,
        created_at=account.created_at,
    )


def get_all_accounts(session: Session) -> list[AccountResponse]:
    accounts = session.query(AccountModel).order_by(AccountModel.id).all()
    return [model_to_schema(account) for account in accounts]


def get_accounts_by_user_id(session: Session, user_id: str) -> list[AccountResponse]:
    accounts = (
        session.query(AccountModel)
        .filter(AccountModel.user_id == user_id)
        .order_by(AccountModel.created_at)
        .all()
    )
    return [model_to_schema(account) for account in accounts]


def get_account_by_id(session: Session, account_id: str) -> AccountResponse | None:
    account = session.get(AccountModel, account_id)

    if account is None:
        return None

    return model_to_schema(account)


def get_account_by_id_and_user_id(
    session: Session,
    account_id: str,
    user_id: str,
) -> AccountResponse | None:
    account = (
        session.query(AccountModel)
        .filter(AccountModel.id == account_id, AccountModel.user_id == user_id)
        .one_or_none()
    )

    if account is None:
        return None

    return model_to_schema(account)


def get_account_by_id_for_update(
    session: Session,
    account_id: str,
) -> AccountResponse | None:
    account = session.query(AccountModel).filter(AccountModel.id == account_id).with_for_update().one_or_none()

    if account is None:
        return None

    return model_to_schema(account)


def save_account(session: Session, account: AccountResponse) -> AccountResponse:
    account_model = AccountModel(
        id=account.id,
        user_id=account.user_id,
        owner_name=account.owner_name,
        balance=account.balance,
        currency=str(account.currency),
        created_at=account.created_at,
    )

    session.add(account_model)
    session.commit()
    session.refresh(account_model)

    return model_to_schema(account_model)


def update_account_balance(
    session: Session,
    account_id: str,
    balance: int,
    *,
    commit: bool = True,
) -> None:
    account = session.get(AccountModel, account_id)

    if account is None:
        return

    account.balance = balance

    if commit:
        session.commit()
