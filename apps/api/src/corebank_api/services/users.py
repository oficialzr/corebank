from datetime import UTC, datetime
from uuid import uuid4

from corebank_api.core.security import create_access_token, hash_password, verify_password
from corebank_api.domain.errors import (
    EmailAlreadyRegisteredError,
    InvalidCredentialsError,
    PhoneAlreadyRegisteredError,
)
from corebank_api.repositories import users_provider
from corebank_api.schemas.user import (
    TokenResponse,
    UserLoginRequest,
    UserRecord,
    UserRegisterRequest,
    UserResponse,
)


def normalize_email(email: str) -> str:
    return email.lower()


def to_user_response(user: UserRecord) -> UserResponse:
    return UserResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        phone_number=user.phone_number,
        is_active=user.is_active,
        created_at=user.created_at,
    )


def register_user(request: UserRegisterRequest) -> UserResponse:
    normalized_email = normalize_email(str(request.email))

    existing_user = users_provider.get_user_by_email(normalized_email)

    if existing_user is not None:
        raise EmailAlreadyRegisteredError

    if users_provider.get_user_by_phone_number(request.phone_number) is not None:
        raise PhoneAlreadyRegisteredError

    user = UserRecord(
        id=f"user-{uuid4()}",
        email=normalized_email,
        password_hash=hash_password(request.password),
        full_name=request.full_name,
        phone_number=request.phone_number,
        is_active=True,
        created_at=datetime.now(UTC),
    )

    saved_user = users_provider.save_user(user)

    return to_user_response(saved_user)


def login_user(request: UserLoginRequest) -> TokenResponse:
    normalized_email = normalize_email(str(request.email))
    user = users_provider.get_user_by_email(normalized_email)

    if user is None or not verify_password(request.password, user.password_hash):
        raise InvalidCredentialsError

    return TokenResponse(
        access_token=create_access_token(user.email),
        token_type="bearer",
    )


def get_user_by_email(email: str) -> UserResponse | None:
    user = users_provider.get_user_by_email(normalize_email(email))

    if user is None:
        return None

    return to_user_response(user)


def update_user_phone_number(user_id: str, phone_number: str) -> UserResponse:
    existing_user = users_provider.get_user_by_phone_number(phone_number)

    if existing_user is not None and existing_user.id != user_id:
        raise PhoneAlreadyRegisteredError

    return to_user_response(users_provider.update_user_phone_number(user_id, phone_number))
