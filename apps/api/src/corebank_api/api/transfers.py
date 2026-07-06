from fastapi import APIRouter, HTTPException, status

from corebank_api.domain.errors import (
    CurrencyMismatchError,
    DestinationAccountNotFoundError,
    InsufficientFundsError,
    SameAccountTransferError,
    SourceAccountNotFoundError,
)
from corebank_api.schemas.transfer import TransferCreateRequest, TransferResponse
from corebank_api.services.transfers import create_transfer

router = APIRouter(prefix="/transfers", tags=["transfers"])


@router.post("", response_model=TransferResponse, status_code=status.HTTP_201_CREATED)
def create_transfer_endpoint(request: TransferCreateRequest) -> TransferResponse:
    try:
        return create_transfer(request)
    except SourceAccountNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Source account not found",
        ) from error
    except DestinationAccountNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Destination account not found",
        ) from error
    except SameAccountTransferError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot transfer to same account",
        ) from error
    except CurrencyMismatchError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Currency mismatch",
        ) from error
    except InsufficientFundsError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient funds",
        ) from error
