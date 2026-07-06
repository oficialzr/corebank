from fastapi import APIRouter, HTTPException, status

from corebank_api.domain.errors import (
    CurrencyMismatchError,
    DestinationAccountNotFoundError,
    InsufficientFundsError,
    SameAccountTransferError,
    SourceAccountNotFoundError,
    TransferError,
)
from corebank_api.schemas.transfer import TransferCreateRequest, TransferResponse
from corebank_api.services.transfers import create_transfer

router = APIRouter(prefix="/transfers", tags=["transfers"])


TRANSFER_ERROR_TO_HTTP_RESPONSE = {
    SourceAccountNotFoundError: (
        status.HTTP_404_NOT_FOUND,
        "Source account not found",
    ),
    DestinationAccountNotFoundError: (
        status.HTTP_404_NOT_FOUND,
        "Destination account not found",
    ),
    SameAccountTransferError: (
        status.HTTP_400_BAD_REQUEST,
        "Cannot transfer to same account",
    ),
    CurrencyMismatchError: (
        status.HTTP_400_BAD_REQUEST,
        "Currency mismatch",
    ),
    InsufficientFundsError: (
        status.HTTP_400_BAD_REQUEST,
        "Insufficient funds",
    ),
}


def map_transfer_error_to_http_exception(error: TransferError) -> HTTPException:
    status_code, detail = TRANSFER_ERROR_TO_HTTP_RESPONSE[type(error)]

    return HTTPException(
        status_code=status_code,
        detail=detail,
    )


@router.post("", response_model=TransferResponse, status_code=status.HTTP_201_CREATED)
def create_transfer_endpoint(request: TransferCreateRequest) -> TransferResponse:
    try:
        return create_transfer(request)
    except TransferError as error:
        raise map_transfer_error_to_http_exception(error) from error