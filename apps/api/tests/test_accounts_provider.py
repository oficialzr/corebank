from corebank_api.repositories import accounts_provider
from corebank_api.schemas.account import AccountResponse


def test_accounts_provider_uses_memory_backend_by_default(monkeypatch) -> None:
    monkeypatch.delenv("COREBANK_REPOSITORY_BACKEND", raising=False)

    account = AccountResponse(
        id="acc-provider-001",
        owner_name="Provider User",
        balance=1000,
        currency="RUB",
    )

    accounts_provider.save_account(account)

    found_account = accounts_provider.get_account_by_id("acc-provider-001")

    assert found_account is not None
    assert found_account.id == "acc-provider-001"
    assert found_account.owner_name == "Provider User"

    accounts_provider.update_account_balance("acc-provider-001", 7777)

    updated_account = accounts_provider.get_account_by_id("acc-provider-001")

    assert updated_account is not None
    assert updated_account.balance == 7777

    accounts = accounts_provider.get_all_accounts()

    assert any(account.id == "acc-provider-001" for account in accounts)