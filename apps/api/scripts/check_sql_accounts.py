from corebank_api.database.session import SessionLocal
from corebank_api.repositories.sql_accounts import (
    get_account_by_id,
    get_all_accounts,
    save_account,
)
from corebank_api.schemas.account import AccountResponse


def main() -> None:
    with SessionLocal() as session:
        account = AccountResponse(
            id="acc-sql-001",
            owner_name="SQL User",
            balance=5000,
            currency="RUB",
        )

        save_account(session, account)

        print(get_account_by_id(session, "acc-sql-001"))
        print(get_all_accounts(session))


if __name__ == "__main__":
    main()
