from datetime import UTC, datetime
from uuid import uuid4

from corebank_api.repositories import accounts_provider as accounts_repository
from corebank_api.schemas.account import AccountCreateRequest, AccountResponse


def list_accounts(user_id: str) -> list[AccountResponse]:
    return accounts_repository.get_accounts_by_user_id(user_id)


def get_account_by_id(account_id: str, user_id: str) -> AccountResponse | None:
    return accounts_repository.get_account_by_id_and_user_id(account_id, user_id)


def create_account(
    request: AccountCreateRequest,
    *,
    user_id: str,
    owner_name: str,
) -> AccountResponse:
    account = AccountResponse(
        id=f"acc-{uuid4()}",
        user_id=user_id,
        owner_name=owner_name,
        balance=0,
        currency=request.currency,
        created_at=datetime.now(UTC),
    )

    return accounts_repository.save_account(account)
