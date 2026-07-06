from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class Currency(StrEnum):
    RUB = "RUB"
    USD = "USD"
    EUR = "EUR"


class AccountCreateRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    owner_name: str = Field(min_length=1)
    currency: Currency


class AccountResponse(BaseModel):
    id: str
    owner_name: str
    balance: int
    currency: str
