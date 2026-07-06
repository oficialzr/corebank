from fastapi import HTTPException

from corebank_api.repositories.accounts import (
    get_account_by_id,
    update_account_balance,
)
from corebank_api.schemas.transfer import (
    TransferCreateRequest,
    TransferResponse,
    TransferStatus,
)


def create_transfer(request: TransferCreateRequest) -> TransferResponse:
    from_account = get_account_by_id(request.from_account_id)
    to_account = get_account_by_id(request.to_account_id)

    if from_account is None:
        raise HTTPException(status_code=404, detail="Source account not found")

    if to_account is None:
        raise HTTPException(status_code=404, detail="Destination account not found")

    if from_account.id == to_account.id:
        raise HTTPException(status_code=400, detail="Cannot transfer to same account")

    if from_account.currency != to_account.currency:
        raise HTTPException(status_code=400, detail="Currency mismatch")

    if from_account.balance < request.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    update_account_balance(from_account.id, from_account.balance - request.amount)
    update_account_balance(to_account.id, to_account.balance + request.amount)

    return TransferResponse(
        from_account_id=from_account.id,
        to_account_id=to_account.id,
        amount=request.amount,
        status=TransferStatus.COMPLETED,
    )
