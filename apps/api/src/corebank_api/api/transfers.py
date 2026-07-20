from typing import Annotated

from fastapi import APIRouter, Header, HTTPException, Query, status

from corebank_api.api.auth import CsrfProtection, CurrentUser
from corebank_api.domain.errors import (
    CurrencyMismatchError,
    DestinationAccountNotFoundError,
    IdempotencyConflictError,
    InsufficientFundsError,
    SameAccountTransferError,
    SourceAccountNotFoundError,
    TransferError,
)
from corebank_api.errors import api_error
from corebank_api.schemas.errors import ErrorResponse
from corebank_api.schemas.transfer import RecipientLookupResponse, TransferCreateRequest, TransferResponse
from corebank_api.services.transfers import create_transfer, get_recipient

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
    IdempotencyConflictError: (
        status.HTTP_409_CONFLICT,
        "idempotency_conflict",
        "Idempotency key was already used for another transfer",
    ),
}


def map_transfer_error_to_http_exception(error: TransferError) -> HTTPException:
    status_code, code, message = TRANSFER_ERROR_TO_HTTP_RESPONSE[type(error)]

    return api_error(
        status_code=status_code,
        code=code,
        message=message,
    )


@router.get(
    "/recipient",
    response_model=RecipientLookupResponse,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse},
    },
)
def get_transfer_recipient_endpoint(
    current_user: CurrentUser,
    from_account_id: str = Query(min_length=1),
    identifier: str = Query(min_length=1, max_length=32),
) -> RecipientLookupResponse:
    try:
        return get_recipient(from_account_id, identifier, current_user.id)
    except TransferError as error:
        raise map_transfer_error_to_http_exception(error) from error


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
def create_transfer_endpoint(
    request: TransferCreateRequest,
    current_user: CurrentUser,
    idempotency_key: Annotated[str, Header(alias="Idempotency-Key", min_length=8, max_length=128)],
    _: CsrfProtection,
) -> TransferResponse:
    try:
        return create_transfer(request, current_user.id, idempotency_key)
    except TransferError as error:
        raise map_transfer_error_to_http_exception(error) from error
