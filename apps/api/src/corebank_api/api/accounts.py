from fastapi import APIRouter, HTTPException

from corebank_api.schemas.account import AccountResponse
from corebank_api.services.accounts import (
    get_account_by_id,
    list_accounts,
)

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("", response_model=list[AccountResponse])
def list_accounts_endpoint() -> list[AccountResponse]:
    return list_accounts()


@router.get("/{account_id}", response_model=AccountResponse)
def get_account_endpoint(account_id: str) -> AccountResponse:
    account = get_account_by_id(account_id)

    if account is None:
        raise HTTPException(
            status_code=404,
            detail="Account not found",
        )

    return account
