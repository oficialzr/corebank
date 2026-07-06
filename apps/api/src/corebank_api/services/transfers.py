from corebank_api.domain.errors import (
    CurrencyMismatchError,
    DestinationAccountNotFoundError,
    InsufficientFundsError,
    SameAccountTransferError,
    SourceAccountNotFoundError,
)
from corebank_api.repositories.accounts import (
    get_account_by_id,
    update_account_balance,
)
from corebank_api.repositories.transactions import save_transaction
from corebank_api.schemas.transaction import TransactionResponse
from corebank_api.schemas.transfer import (
    TransferCreateRequest,
    TransferResponse,
    TransferStatus,
)


def create_transfer(request: TransferCreateRequest) -> TransferResponse:
    from_account = get_account_by_id(request.from_account_id)
    to_account = get_account_by_id(request.to_account_id)

    if from_account is None:
        raise SourceAccountNotFoundError

    if to_account is None:
        raise DestinationAccountNotFoundError

    if from_account.id == to_account.id:
        raise SameAccountTransferError

    if from_account.currency != to_account.currency:
        raise CurrencyMismatchError

    if from_account.balance < request.amount:
        raise InsufficientFundsError

    update_account_balance(from_account.id, from_account.balance - request.amount)
    update_account_balance(to_account.id, to_account.balance + request.amount)

    transaction_id = "tx-001"

    transaction = save_transaction(
        TransactionResponse(
            id=transaction_id,
            from_account_id=from_account.id,
            to_account_id=to_account.id,
            amount=request.amount,
            currency=from_account.currency,
            status=TransferStatus.COMPLETED,
        ),
    )

    return TransferResponse(
        transaction_id=transaction.id,
        from_account_id=from_account.id,
        to_account_id=to_account.id,
        amount=request.amount,
        status=TransferStatus.COMPLETED,
    )
