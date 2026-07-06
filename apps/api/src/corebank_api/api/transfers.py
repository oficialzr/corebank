from fastapi import APIRouter, status

from corebank_api.schemas.transfer import TransferCreateRequest, TransferResponse
from corebank_api.services.transfers import create_transfer

router = APIRouter(prefix="/transfers", tags=["transfers"])


@router.post("", response_model=TransferResponse, status_code=status.HTTP_201_CREATED)
def create_transfer_endpoint(request: TransferCreateRequest) -> TransferResponse:
    return create_transfer(request)
