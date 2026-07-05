from fastapi import APIRouter

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("")
def list_accounts() -> list[dict[str, str | int]]:
    return [
        {
            "id": "acc-001",
            "owner_name": "Alex Ivanov",
            "balance": 100000,
            "currency": "RUB",
        },
        {
            "id": "acc-002",
            "owner_name": "Maria Petrova",
            "balance": 250000,
            "currency": "RUB",
        },
    ]