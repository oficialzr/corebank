from fastapi import APIRouter, HTTPException, status

from corebank_api.domain.errors import (
    CurrencyMismatchError,
    DestinationAccountNotFoundError,
    InsufficientFundsError,
    SameAccountTransferError,
    SourceAccountNotFoundError,
    TransferError,
)
from corebank_api.errors import api_error
from corebank_api.schemas.errors import ErrorResponse
from corebank_api.schemas.transfer import TransferCreateRequest, TransferResponse
from corebank_api.services.transfers import create_transfer

router = APIRouter(prefix="/transfers", tags=["Transfers"])


TRANSFER_ERROR_TO_HTTP_RESPONSE = {
    SourceAccountNotFoundError: (
        status.HTTP_404_NOT_FOUND,
        "source_account_not_found",
        "Source account not found",
    ),
    DestinationAccountNotFoundError: (
        status.HTTP_404_NOT_FOUND,
        "destination_account_not_found",
        "Destination account not found",
    ),
    SameAccountTransferError: (
        status.HTTP_400_BAD_REQUEST,
        "same_account_transfer",
        "Cannot transfer to same account",
    ),
    CurrencyMismatchError: (
        status.HTTP_400_BAD_REQUEST,
        "currency_mismatch",
        "Currency mismatch",
    ),
    InsufficientFundsError: (
        status.HTTP_400_BAD_REQUEST,
        "insufficient_funds",
        "Insufficient funds",
    ),
}


def map_transfer_error_to_http_exception(error: TransferError) -> HTTPException:
    status_code, code, message = TRANSFER_ERROR_TO_HTTP_RESPONSE[type(error)]

    return api_error(
        status_code=status_code,
        code=code,
        message=message,
    )


@router.post(
    "",
    response_model=TransferResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse,
            "description": ("Invalid transfer: same account, insufficient funds or currency mismatch"),
        },
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorResponse,
            "description": "Source or destination account not found",
        },
    },
)
def create_transfer_endpoint(request: TransferCreateRequest) -> TransferResponse:
    try:
        return create_transfer(request)
    except TransferError as error:
        raise map_transfer_error_to_http_exception(error) from error
