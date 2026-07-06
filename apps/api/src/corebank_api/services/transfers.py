from datetime import UTC, datetime

from corebank_api.domain.errors import (
    CurrencyMismatchError,
    DestinationAccountNotFoundError,
    InsufficientFundsError,
    SameAccountTransferError,
    SourceAccountNotFoundError,
)
from corebank_api.database.session import SessionLocal
from corebank_api.repositories import sql_accounts, sql_transactions
from corebank_api.schemas.transaction import TransactionResponse
from corebank_api.schemas.transfer import (
    TransferCreateRequest,
    TransferResponse,
    TransferStatus,
)


def create_transfer(request: TransferCreateRequest) -> TransferResponse:
    with SessionLocal() as session:
        from_account = sql_accounts.get_account_by_id(
            session,
            request.from_account_id,
        )
        to_account = sql_accounts.get_account_by_id(
            session,
            request.to_account_id,
        )

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

        sql_accounts.update_account_balance(
            session,
            from_account.id,
            from_account.balance - request.amount,
            commit=False,
        )
        sql_accounts.update_account_balance(
            session,
            to_account.id,
            to_account.balance + request.amount,
            commit=False,
        )

        transaction_id = sql_transactions.generate_transaction_id(session)

        transaction = sql_transactions.save_transaction(
            session,
            TransactionResponse(
                id=transaction_id,
                from_account_id=from_account.id,
                to_account_id=to_account.id,
                amount=request.amount,
                currency=from_account.currency,
                status=TransferStatus.COMPLETED,
                created_at=datetime.now(UTC),
            ),
            commit=False,
        )

        session.commit()

        return TransferResponse(
            transaction_id=transaction.id,
            from_account_id=from_account.id,
            to_account_id=to_account.id,
            amount=request.amount,
            status=TransferStatus.COMPLETED,
        )
