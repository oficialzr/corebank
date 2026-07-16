from datetime import UTC, datetime

import pytest
from corebank_api.repositories import users_provider
from corebank_api.schemas.user import UserRecord

pytestmark = pytest.mark.db


def make_user() -> UserRecord:
    return UserRecord(
        id="user-001",
        email="alex@example.com",
        password_hash="hashed-password",
        full_name="Alex Ivanov",
        is_active=True,
        created_at=datetime.now(UTC),
    )


def test_save_user_repository_saves_user() -> None:
    user = make_user()

    saved_user = users_provider.save_user(user)

    assert saved_user == user


def test_get_user_by_email_returns_user() -> None:
    user = users_provider.save_user(make_user())

    found_user = users_provider.get_user_by_email(user.email)

    assert found_user == user


def test_get_user_by_email_returns_none_for_unknown_email() -> None:
    found_user = users_provider.get_user_by_email("unknown@example.com")

    assert found_user is None
