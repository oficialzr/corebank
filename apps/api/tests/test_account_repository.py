from corebank_api.repositories.accounts import get_account_by_id, get_all_accounts


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
