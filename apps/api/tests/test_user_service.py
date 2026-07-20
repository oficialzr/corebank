import pytest
from corebank_api.core.security import verify_password
from corebank_api.domain.errors import EmailAlreadyRegisteredError, InvalidCredentialsError
from corebank_api.repositories import users_provider
from corebank_api.schemas.user import UserLoginRequest, UserRegisterRequest
from corebank_api.services.users import login_user, register_user

pytestmark = pytest.mark.db


def make_request(email: str = "Alex@Example.com") -> UserRegisterRequest:
    return UserRegisterRequest(
        email=email,
        password="strong-password",
        full_name="Alex Ivanov",
        phone_number="+79991234567",
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


def test_login_user_returns_authenticated_user() -> None:
    register_user(make_request())

    response = login_user(
        UserLoginRequest(
            email="alex@example.com",
            password="strong-password",
        )
    )

    assert response.email == "alex@example.com"


def test_login_user_rejects_invalid_password() -> None:
    register_user(make_request())

    with pytest.raises(InvalidCredentialsError):
        login_user(
            UserLoginRequest(
                email="alex@example.com",
                password="wrong-password",
            )
        )
