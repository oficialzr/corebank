from fastapi import APIRouter, HTTPException, status

from corebank_api.domain.errors import EmailAlreadyRegisteredError
from corebank_api.errors import api_error
from corebank_api.schemas.errors import ErrorResponse
from corebank_api.schemas.user import UserRegisterRequest, UserResponse
from corebank_api.services.users import register_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


def email_already_registered_error() -> HTTPException:
    return api_error(
        status_code=status.HTTP_409_CONFLICT,
        code="email_already_registered",
        message="Email is already registered",
    )


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {
            "model": ErrorResponse,
            "description": "Email is already registered",
        },
    },
)
def register_user_endpoint(
    request: UserRegisterRequest,
) -> UserResponse:
    try:
        return register_user(request)
    except EmailAlreadyRegisteredError as error:
        raise email_already_registered_error() from error
