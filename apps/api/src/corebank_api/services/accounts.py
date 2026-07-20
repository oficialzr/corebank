from datetime import UTC, datetime
from secrets import randbelow
from uuid import uuid4

from corebank_api.repositories import accounts_provider as accounts_repository
from corebank_api.schemas.account import AccountCreateRequest, AccountResponse


def add_luhn_check_digit(number: str) -> str:
    digits = [int(digit) for digit in number]
    total = 0
    parity = (len(digits) + 1) % 2

    for index, digit in enumerate(digits):
        if index % 2 == parity:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit

    return f"{number}{(10 - total % 10) % 10}"


def generate_card_number() -> str:
    while True:
        candidate = add_luhn_check_digit(f"2200{randbelow(10**11):011d}")
        if accounts_repository.get_account_by_card_number(candidate) is None:
            return candidate


def list_accounts(user_id: str) -> list[AccountResponse]:
    return accounts_repository.get_accounts_by_user_id(user_id)


def get_account_by_id(account_id: str, user_id: str) -> AccountResponse | None:
    return accounts_repository.get_account_by_id_and_user_id(account_id, user_id)


def create_account(
    request: AccountCreateRequest,
    *,
    user_id: str,
    owner_name: str,
) -> AccountResponse:
    account = AccountResponse(
        id=f"acc-{uuid4()}",
        user_id=user_id,
        owner_name=owner_name,
        card_number=generate_card_number(),
        balance="0.00",
        currency=request.currency,
        created_at=datetime.now(UTC),
    )

    return accounts_repository.save_account(account)
