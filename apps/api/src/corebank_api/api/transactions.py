from fastapi import APIRouter, Query, status

from corebank_api.errors import api_error
from corebank_api.schemas.errors import ErrorResponse
from corebank_api.schemas.transaction import TransactionResponse
from corebank_api.services.transactions import (
    get_transaction,
    list_transactions,
    list_transactions_by_account_id,
)

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.get(
    "",
    response_model=list[TransactionResponse],
    responses={
        status.HTTP_422_UNPROCESSABLE_CONTENT: {
            "model": ErrorResponse,
            "description": "Account ID must not be blank",
        }
    },
)
def list_transactions_endpoint(
    account_id: str | None = Query(default=None, min_length=1),
) -> list[TransactionResponse]:
    if account_id is not None:
        account_id = account_id.strip()

        if not account_id:
            raise api_error(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                code="account_id_must_not_be_blank",
                message="Account ID must not be blank",
            )

        return list_transactions_by_account_id(account_id)

    return list_transactions()


@router.get(
    "/{transaction_id}",
    response_model=TransactionResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Transaction not found",
        }
    },
)
def get_transaction_endpoint(transaction_id: str) -> TransactionResponse:
    transaction = get_transaction(transaction_id)

    if transaction is None:
        raise api_error(
            status_code=status.HTTP_404_NOT_FOUND,
            code="transaction_not_found",
            message="Transaction not found",
        )

    return transaction
