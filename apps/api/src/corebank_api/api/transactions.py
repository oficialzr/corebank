from fastapi import APIRouter, HTTPException, status

from corebank_api.schemas.transaction import TransactionResponse
from corebank_api.services.transactions import get_transaction, list_transactions

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("", response_model=list[TransactionResponse])
def list_transactions_endpoint() -> list[TransactionResponse]:
    return list_transactions()


@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction_endpoint(transaction_id: str) -> TransactionResponse:
    transaction = get_transaction(transaction_id)

    if transaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found",
        )

    return transaction
