from datetime import UTC, datetime
from uuid import uuid4

from corebank_api.core.security import hash_password
from corebank_api.domain.errors import EmailAlreadyRegisteredError
from corebank_api.repositories import users_provider
from corebank_api.schemas.user import (
    UserRecord,
    UserRegisterRequest,
    UserResponse,
)


def register_user(request: UserRegisterRequest) -> UserResponse:
    normalized_email = str(request.email).lower()

    existing_user = users_provider.get_user_by_email(normalized_email)

    if existing_user is not None:
        raise EmailAlreadyRegisteredError

    user = UserRecord(
        id=f"user-{uuid4()}",
        email=normalized_email,
        password_hash=hash_password(request.password),
        full_name=request.full_name,
        is_active=True,
        created_at=datetime.now(UTC),
    )

    saved_user = users_provider.save_user(user)

    return UserResponse(
        id=saved_user.id,
        email=saved_user.email,
        full_name=saved_user.full_name,
        is_active=saved_user.is_active,
        created_at=saved_user.created_at,
    )
