from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


def normalize_phone_number(value: str) -> str:
    compact = "".join(character for character in value if character.isdigit() or character == "+")
    digits = compact.lstrip("+")

    if len(digits) == 11 and digits.startswith("8"):
        return f"+7{digits[1:]}"
    if len(digits) == 11 and digits.startswith("7"):
        return f"+{digits}"
    return f"+{digits}" if digits else compact


class UserRecord(BaseModel):
    id: str
    email: str
    password_hash: str
    full_name: str
    phone_number: str | None
    is_active: bool
    is_admin: bool = False
    created_at: datetime


class UserRegisterRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=1, max_length=200)
    phone_number: str = Field(pattern=r"^\+[1-9]\d{7,14}$")

    @field_validator("phone_number", mode="before")
    @classmethod
    def normalize_phone(cls, value: str) -> str:
        return normalize_phone_number(value)


class UserLoginRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserPhoneUpdateRequest(BaseModel):
    phone_number: str = Field(pattern=r"^\+[1-9]\d{7,14}$")

    @field_validator("phone_number", mode="before")
    @classmethod
    def normalize_phone(cls, value: str) -> str:
        return normalize_phone_number(value)


class UserResponse(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    phone_number: str | None
    is_active: bool
    is_admin: bool
    created_at: datetime


class SessionResponse(BaseModel):
    authenticated: bool
