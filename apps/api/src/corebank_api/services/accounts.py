from corebank_api.repositories import accounts_provider as accounts_repository
from corebank_api.schemas.account import AccountCreateRequest, AccountResponse


def list_accounts() -> list[AccountResponse]:
    return accounts_repository.get_all_accounts()


def get_account_by_id(account_id: str) -> AccountResponse | None:
    return accounts_repository.get_account_by_id(account_id)


def create_account(request: AccountCreateRequest) -> AccountResponse:
    accounts = accounts_repository.get_all_accounts()
    next_number = len(accounts) + 1

    account = AccountResponse(
        id=f"acc-{next_number:03}",
        owner_name=request.owner_name,
        balance=0,
        currency=request.currency,
    )

    return accounts_repository.save_account(account)
