import base64
import hashlib
import hmac
import json
from datetime import UTC, datetime, timedelta

from pwdlib import PasswordHash

from corebank_api.core.config import settings

password_hash = PasswordHash.recommended()
SUPPORTED_JWT_ALGORITHM = "HS256"


class InvalidTokenError(Exception):
    pass


def _base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _base64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def _sign(message: bytes) -> str:
    return _base64url_encode(
        hmac.new(
            settings.jwt_secret_key.encode("utf-8"),
            message,
            hashlib.sha256,
        ).digest()
    )


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def create_access_token(subject: str) -> str:
    if settings.jwt_algorithm != SUPPORTED_JWT_ALGORITHM:
        raise ValueError(f"Unsupported JWT algorithm: {settings.jwt_algorithm}")

    now = datetime.now(UTC)
    expires_at = now + timedelta(minutes=settings.access_token_expire_minutes)

    header = {
        "alg": settings.jwt_algorithm,
        "typ": "JWT",
    }
    payload = {
        "sub": subject,
        "exp": int(expires_at.timestamp()),
    }

    encoded_header = _base64url_encode(json.dumps(header, separators=(",", ":"), sort_keys=True).encode("utf-8"))
    encoded_payload = _base64url_encode(json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8"))
    signing_input = f"{encoded_header}.{encoded_payload}".encode("ascii")
    signature = _sign(signing_input)

    return f"{encoded_header}.{encoded_payload}.{signature}"


def decode_access_token(token: str) -> str:
    try:
        encoded_header, encoded_payload, signature = token.split(".")
    except ValueError as error:
        raise InvalidTokenError from error

    signing_input = f"{encoded_header}.{encoded_payload}".encode("ascii")
    expected_signature = _sign(signing_input)

    if not hmac.compare_digest(signature, expected_signature):
        raise InvalidTokenError

    try:
        header = json.loads(_base64url_decode(encoded_header))
        payload = json.loads(_base64url_decode(encoded_payload))
    except (ValueError, json.JSONDecodeError) as error:
        raise InvalidTokenError from error

    if header.get("alg") != SUPPORTED_JWT_ALGORITHM:
        raise InvalidTokenError

    expires_at = payload.get("exp")
    subject = payload.get("sub")

    if not isinstance(expires_at, int) or not isinstance(subject, str) or not subject:
        raise InvalidTokenError

    if datetime.now(UTC).timestamp() >= expires_at:
        raise InvalidTokenError

    return subject
