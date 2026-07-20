from datetime import UTC, datetime

from corebank_api.database.session import SessionLocal
from corebank_api.domain.errors import (
    CurrencyMismatchError,
    DestinationAccountNotFoundError,
    InsufficientFundsError,
    SameAccountTransferError,
    SourceAccountNotFoundError,
)
from corebank_api.repositories import sql_accounts, sql_transactions
from corebank_api.schemas.transaction import TransactionResponse
from corebank_api.schemas.transfer import (
    RecipientLookupResponse,
    TransferCreateRequest,
    TransferResponse,
    TransferStatus,
)
from corebank_api.schemas.user import normalize_phone_number


def normalize_recipient_identifier(identifier: str) -> tuple[str, str]:
    digits = "".join(character for character in identifier if character.isdigit())

    if len(digits) == 16:
        return "card", digits

    return "phone", normalize_phone_number(identifier)


def resolve_recipient_account(session, identifier: str, currency: str):
    identifier_type, normalized = normalize_recipient_identifier(identifier)

    if identifier_type == "card":
        account = sql_accounts.get_account_by_card_number(session, normalized)
        if account is not None and account.currency != currency:
            raise CurrencyMismatchError
        return account

    return sql_accounts.get_recipient_account_by_phone(session, normalized, currency)


def get_recipient(
    from_account_id: str,
    identifier: str,
    user_id: str,
) -> RecipientLookupResponse:
    with SessionLocal() as session:
        from_account = sql_accounts.get_account_by_id(session, from_account_id)

        if from_account is None or from_account.user_id != user_id:
            raise SourceAccountNotFoundError

        recipient = resolve_recipient_account(session, identifier, from_account.currency)

        if recipient is None:
            raise DestinationAccountNotFoundError
        if recipient.id == from_account.id:
            raise SameAccountTransferError

        return RecipientLookupResponse(
            display_name=recipient.owner_name,
            masked_card_number=f"•••• {recipient.card_number[-4:]}",
            currency=recipient.currency,
        )


def create_transfer(request: TransferCreateRequest, user_id: str) -> TransferResponse:
    with SessionLocal() as session:
        source = sql_accounts.get_account_by_id(session, request.from_account_id)

        if source is None or source.user_id != user_id:
            raise SourceAccountNotFoundError

        if request.to_account_id is not None:
            destination_account_id = request.to_account_id
        else:
            recipient = resolve_recipient_account(session, request.recipient or "", source.currency)
            if recipient is None:
                raise DestinationAccountNotFoundError
            destination_account_id = recipient.id

        account_ids_to_lock = sorted(
            [
                request.from_account_id,
                destination_account_id,
            ]
        )

        locked_accounts = {}

        for account_id in account_ids_to_lock:
            locked_account = sql_accounts.get_account_by_id_for_update(
                session,
                account_id,
            )
            locked_accounts[account_id] = locked_account

        from_account = locked_accounts[request.from_account_id]
        to_account = locked_accounts[destination_account_id]

        if from_account is None:
            raise SourceAccountNotFoundError

        if from_account.user_id != user_id:
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
