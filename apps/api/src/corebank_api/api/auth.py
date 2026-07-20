import hmac
import secrets
from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, Request, Response, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from corebank_api.core.security import InvalidTokenError, create_access_token, decode_access_token
from corebank_api.domain.errors import (
    EmailAlreadyRegisteredError,
    InvalidCredentialsError,
    PhoneAlreadyRegisteredError,
)
from corebank_api.errors import api_error
from corebank_api.schemas.errors import ErrorResponse
from corebank_api.schemas.user import (
    SessionResponse,
    UserLoginRequest,
    UserPhoneUpdateRequest,
    UserRegisterRequest,
    UserResponse,
)
from corebank_api.services.audit import append_audit_event
from corebank_api.services.users import (
    get_user_by_email,
    login_user,
    register_user,
    update_user_phone_number,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])
bearer_scheme = HTTPBearer(auto_error=False)
BearerCredentials = Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)]
ACCESS_COOKIE = "corebank_session"
CSRF_COOKIE = "corebank_csrf"


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


def phone_already_registered_error() -> HTTPException:
    return api_error(
        status_code=status.HTTP_409_CONFLICT,
        code="phone_already_registered",
        message="Phone number is already registered",
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


def get_current_user(request: Request, credentials: BearerCredentials) -> UserResponse:
    token = request.cookies.get(ACCESS_COOKIE)
    if token is None and credentials is not None and credentials.scheme.lower() == "bearer":
        token = credentials.credentials
    if token is None:
        raise invalid_token_error()

    try:
        email = decode_access_token(token)
    except InvalidTokenError as error:
        raise invalid_token_error() from error

    user = get_user_by_email(email)

    if user is None:
        raise invalid_token_error()

    return user


CurrentUser = Annotated[UserResponse, Depends(get_current_user)]


def validate_csrf(
    request: Request,
    csrf_header: Annotated[str | None, Header(alias="X-CSRF-Token")] = None,
) -> None:
    if request.cookies.get(ACCESS_COOKIE) is None:
        return
    csrf_cookie = request.cookies.get(CSRF_COOKIE)
    if csrf_cookie is None or csrf_header is None or not hmac.compare_digest(csrf_cookie, csrf_header):
        raise api_error(status.HTTP_403_FORBIDDEN, "invalid_csrf", "Invalid CSRF token")


CsrfProtection = Annotated[None, Depends(validate_csrf)]


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
    except PhoneAlreadyRegisteredError as error:
        raise phone_already_registered_error() from error


@router.post(
    "/login",
    response_model=SessionResponse,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": ErrorResponse,
            "description": "Invalid email or password",
        },
    },
)
def login_user_endpoint(request: UserLoginRequest, response: Response) -> SessionResponse:
    try:
        user = login_user(request)
    except InvalidCredentialsError as error:
        raise invalid_credentials_error() from error
    access_token = create_access_token(user.email)
    csrf_token = secrets.token_urlsafe(32)
    response.set_cookie(ACCESS_COOKIE, access_token, httponly=True, secure=True, samesite="strict", path="/")
    response.set_cookie(CSRF_COOKIE, csrf_token, httponly=False, secure=True, samesite="strict", path="/")
    append_audit_event("auth.login", user_id=user.id, entity_type="user", entity_id=user.id)
    return SessionResponse(authenticated=True)


@router.post("/logout", response_model=SessionResponse)
def logout_user_endpoint(response: Response, _: CsrfProtection) -> SessionResponse:
    response.delete_cookie(ACCESS_COOKIE, secure=True, httponly=True, samesite="strict", path="/")
    response.delete_cookie(CSRF_COOKIE, secure=True, httponly=False, samesite="strict", path="/")
    return SessionResponse(authenticated=False)


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


@router.patch(
    "/me/phone",
    response_model=UserResponse,
    responses={status.HTTP_409_CONFLICT: {"model": ErrorResponse}},
)
def update_current_user_phone_endpoint(
    request: UserPhoneUpdateRequest,
    current_user: CurrentUser,
    _: CsrfProtection,
) -> UserResponse:
    try:
        user = update_user_phone_number(current_user.id, request.phone_number)
        append_audit_event("user.phone_updated", user_id=user.id, entity_type="user", entity_id=user.id)
        return user
    except PhoneAlreadyRegisteredError as error:
        raise phone_already_registered_error() from error
