from corebank_api.repositories.accounts import (
    get_account_by_id,
    get_all_accounts,
    update_account_balance,
)
from corebank_api.repositories.transactions import (
    generate_transaction_id,
    get_all_transactions,
    get_transaction_by_id,
    save_transaction,
)
from corebank_api.schemas.common import Currency
from corebank_api.schemas.transaction import TransactionResponse
from corebank_api.schemas.transfer import TransferStatus


def test_get_all_accounts_repository_returns_accounts() -> None:
    accounts = get_all_accounts()

    assert len(accounts) == 2
    assert accounts[0].id == "acc-001"


def test_get_account_by_id_repository_returns_account() -> None:
    account = get_account_by_id("acc-001")

    assert account is not None
    assert account.id == "acc-001"
    assert account.owner_name == "Alex Ivanov"


def test_get_account_by_id_repository_returns_none_for_unknown_account() -> None:
    account = get_account_by_id("acc-999")

    assert account is None


def test_update_account_balance_repository_updates_balance() -> None:
    update_account_balance("acc-001", 77777)

    account = get_account_by_id("acc-001")

    assert account is not None
    assert account.balance == 77777


def test_update_account_balance_repository_does_nothing_for_unknown_account() -> None:
    update_account_balance("acc-999", 77777)

    account = get_account_by_id("acc-999")

    assert account is None


def test_save_transaction_repository_saves_transaction() -> None:
    transaction = TransactionResponse(
        id="tx-001",
        from_account_id="acc-001",
        to_account_id="acc-002",
        amount=1000,
        currency=Currency.RUB,
        status=TransferStatus.COMPLETED,
    )

    save_transaction(transaction)

    transactions = get_all_transactions()

    assert len(transactions) == 1
    assert transactions[0].id == "tx-001"


def test_get_transaction_by_id_repository_returns_transaction() -> None:
    transaction = TransactionResponse(
        id="tx-001",
        from_account_id="acc-001",
        to_account_id="acc-002",
        amount=1000,
        currency=Currency.RUB,
        status=TransferStatus.COMPLETED,
    )

    save_transaction(transaction)

    found_transaction = get_transaction_by_id("tx-001")

    assert found_transaction is not None
    assert found_transaction.id == "tx-001"


def test_get_transaction_by_id_repository_returns_none_for_unknown_transaction() -> (
    None
):
    transaction = get_transaction_by_id("tx-999")

    assert transaction is None


def test_generate_transaction_id_repository_returns_next_id() -> None:
    first_transaction_id = generate_transaction_id()

    transaction = TransactionResponse(
        id=first_transaction_id,
        from_account_id="acc-001",
        to_account_id="acc-002",
        amount=1000,
        currency=Currency.RUB,
        status=TransferStatus.COMPLETED,
    )

    save_transaction(transaction)

    second_transaction_id = generate_transaction_id()

    assert first_transaction_id == "tx-001"
    assert second_transaction_id == "tx-002"
