from corebank_api.repositories import accounts as accounts_repository
from corebank_api.schemas.account import AccountResponse


def list_accounts() -> list[AccountResponse]:
    return accounts_repository.get_all_accounts()


def get_account_by_id(account_id: str) -> AccountResponse | None:
    return accounts_repository.get_account_by_id(account_id)
