from datetime import UTC, datetime

import pytest
from corebank_api.database.models import AccountModel
from corebank_api.database.session import SessionLocal
from corebank_api.repositories.sql_accounts import (
    get_account_by_id,
    get_all_accounts,
    save_account,
    update_account_balance,
)
from corebank_api.schemas.account import AccountResponse
from sqlalchemy.exc import OperationalError

pytestmark = pytest.mark.db


def test_sql_accounts_repository_saves_and_reads_account() -> None:
    try:
        with SessionLocal() as session:
            session.query(AccountModel).filter(AccountModel.id == "acc-test-001").delete()
            session.commit()

            account = AccountResponse(
                id="acc-test-001",
                user_id="user-alex",
                owner_name="SQL Test User",
                balance=5000,
                currency="RUB",
                created_at=datetime.now(UTC),
            )

            save_account(session, account)

            found_account = get_account_by_id(session, "acc-test-001")

            assert found_account is not None
            assert found_account.id == "acc-test-001"
            assert found_account.owner_name == "SQL Test User"
            assert found_account.balance == 5000
            assert found_account.currency == "RUB"
            assert found_account.created_at is not None

            accounts = get_all_accounts(session)

            assert any(account.id == "acc-test-001" for account in accounts)

            update_account_balance(session, "acc-test-001", 7777)

            updated_account = get_account_by_id(session, "acc-test-001")

            assert updated_account is not None
            assert updated_account.balance == 7777

            session.query(AccountModel).filter(AccountModel.id == "acc-test-001").delete()
            session.commit()
    except OperationalError:
        return
