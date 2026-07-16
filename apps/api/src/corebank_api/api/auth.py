from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from corebank_api.core.security import InvalidTokenError, decode_access_token
from corebank_api.domain.errors import EmailAlreadyRegisteredError, InvalidCredentialsError
from corebank_api.errors import api_error
from corebank_api.schemas.errors import ErrorResponse
from corebank_api.schemas.user import (
    TokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)
from corebank_api.services.users import get_user_by_email, login_user, register_user

router = APIRouter(prefix="/auth", tags=["Authentication"])
bearer_scheme = HTTPBearer(auto_error=False)
BearerCredentials = Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)]


def email_already_registered_error() -> HTTPException:
    return api_error(
        status_code=status.HTTP_409_CONFLICT,
        code="email_already_registered",
        message="Email is already registered",
    )


def invalid_credentials_error() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "code": "invalid_credentials",
            "message": "Invalid email or password",
        },
        headers={"WWW-Authenticate": "Bearer"},
    )


def invalid_token_error() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "code": "invalid_token",
            "message": "Invalid or expired access token",
        },
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_current_user(credentials: BearerCredentials) -> UserResponse:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise invalid_token_error()

    try:
        email = decode_access_token(credentials.credentials)
    except InvalidTokenError as error:
        raise invalid_token_error() from error

    user = get_user_by_email(email)

    if user is None:
        raise invalid_token_error()

    return user


CurrentUser = Annotated[UserResponse, Depends(get_current_user)]


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


@router.post(
    "/login",
    response_model=TokenResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "Invalid email or password",
        },
    },
)
def login_user_endpoint(request: UserLoginRequest) -> TokenResponse:
    try:
        return login_user(request)
    except InvalidCredentialsError as error:
        raise invalid_credentials_error() from error


@router.get(
    "/me",
    response_model=UserResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "Invalid or expired access token",
        },
    },
)
def get_current_user_endpoint(current_user: CurrentUser) -> UserResponse:
    return current_user
