from fastapi import APIRouter, HTTPException

from corebank_api.schemas.account import AccountResponse

router = APIRouter(prefix="/accounts", tags=["accounts"])


ACCOUNTS = [
    AccountResponse(
        id="acc-001",
        owner_name="Alex Ivanov",
        balance=100000,
        currency="RUB",
    ),
    AccountResponse(
        id="acc-002",
        owner_name="Maria Petrova",
        balance=250000,
        currency="RUB",
    ),
]


@router.get("", response_model=list[AccountResponse])
def list_accounts() -> list[AccountResponse]:
    return ACCOUNTS


@router.get("/{account_id}", response_model=AccountResponse)
def get_account(account_id: str) -> AccountResponse:
    for account in ACCOUNTS:
        if account.id == account_id:
            return account

    raise HTTPException(
        status_code=404,
        detail="Account not found",
    )