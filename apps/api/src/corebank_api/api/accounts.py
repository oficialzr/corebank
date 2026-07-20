from fastapi import APIRouter, status

from corebank_api.api.auth import CurrentUser
from corebank_api.errors import api_error
from corebank_api.schemas.account import AccountCreateRequest, AccountResponse
from corebank_api.schemas.errors import ErrorResponse
from corebank_api.services.accounts import (
    create_account,
    get_account_by_id,
    list_accounts,
)

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.get("", response_model=list[AccountResponse])
def list_accounts_endpoint(current_user: CurrentUser) -> list[AccountResponse]:
    return list_accounts(current_user.id)


@router.get(
    "/{account_id}",
    response_model=AccountResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Account not found",
        }
    },
)
def get_account_endpoint(account_id: str, current_user: CurrentUser) -> AccountResponse:
    account = get_account_by_id(account_id, current_user.id)

    if account is None:
        raise api_error(
            status_code=404,
            code="account_not_found",
            message="Account not found",
        )

    return account


@router.post("", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
def create_account_endpoint(request: AccountCreateRequest, current_user: CurrentUser) -> AccountResponse:
    return create_account(
        request,
        user_id=current_user.id,
        owner_name=current_user.full_name,
    )
