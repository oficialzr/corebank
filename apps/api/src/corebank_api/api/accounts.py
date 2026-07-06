from fastapi import APIRouter

from corebank_api.schemas.account import AccountResponse

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("", response_model=list[AccountResponse])
def list_accounts() -> list[AccountResponse]:
    return [
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