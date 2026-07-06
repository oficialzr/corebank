from corebank_api.schemas.account import AccountCreateRequest
from corebank_api.services.accounts import (
    create_account,
    get_account_by_id,
    list_accounts,
)


def test_list_accounts_service_returns_accounts() -> None:
    accounts = list_accounts()

    assert len(accounts) >= 2
    assert accounts[0].id == "acc-001"


def test_get_account_by_id_service_returns_account() -> None:
    account = get_account_by_id("acc-001")

    assert account is not None
    assert account.id == "acc-001"
    assert account.owner_name == "Alex Ivanov"


def test_get_account_by_id_service_returns_none_for_unknown_account() -> None:
    account = get_account_by_id("acc-999")

    assert account is None


def test_create_account_service_creates_account() -> None:
    request = AccountCreateRequest(
        owner_name="Ivan Sidorov",
        currency="RUB",
    )

    account = create_account(request)

    assert account.id.startswith("acc-")
    assert account.owner_name == "Ivan Sidorov"
    assert account.balance == 0
    assert account.currency == "RUB"
