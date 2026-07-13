import pytest
from corebank_api.core.security import verify_password
from corebank_api.domain.errors import EmailAlreadyRegisteredError
from corebank_api.repositories import users_provider
from corebank_api.schemas.user import UserRegisterRequest
from corebank_api.services.users import register_user


def make_request(email: str = "Alex@Example.com") -> UserRegisterRequest:
    return UserRegisterRequest(
        email=email,
        password="strong-password",
        full_name="Alex Ivanov",
    )


def test_register_user_creates_user() -> None:
    response = register_user(make_request())

    assert response.id.startswith("user-")
    assert response.email == "alex@example.com"
    assert response.full_name == "Alex Ivanov"
    assert response.is_active is True


def test_register_user_hashes_password() -> None:
    register_user(make_request())

    stored_user = users_provider.get_user_by_email("alex@example.com")

    assert stored_user is not None
    assert stored_user.password_hash != "strong-password"
    assert verify_password(
        "strong-password",
        stored_user.password_hash,
    )


def test_register_user_rejects_duplicate_email() -> None:
    register_user(make_request())

    with pytest.raises(EmailAlreadyRegisteredError):
        register_user(make_request("alex@example.com"))
