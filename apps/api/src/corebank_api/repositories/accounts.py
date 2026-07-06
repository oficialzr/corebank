from corebank_api.schemas.account import AccountResponse


_INITIAL_ACCOUNTS = [
    AccountResponse(
        id="acc-001",
        owner_name="Alex Ivanov",
        balance=100000,
        currency="RUB",
    ),
    AccountResponse(
        id="acc-002",
        owner_name="Maria Petrova",
        balance=250000,
        currency="USD",
    ),
]

ACCOUNTS = list(_INITIAL_ACCOUNTS)


def reset_accounts_repository() -> None:
    ACCOUNTS.clear()
    ACCOUNTS.extend(_INITIAL_ACCOUNTS)


def get_all_accounts() -> list[AccountResponse]:
    return ACCOUNTS


def get_account_by_id(account_id: str) -> AccountResponse | None:
    for account in ACCOUNTS:
        if account.id == account_id:
            return account

    return None


def save_account(account: AccountResponse) -> AccountResponse:
    ACCOUNTS.append(account)
    return account