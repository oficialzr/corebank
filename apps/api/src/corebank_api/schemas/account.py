from typing import Literal

from pydantic import BaseModel, Field


class AccountCreateRequest(BaseModel):
    owner_name: str = Field(min_length=1)
    currency: Literal["RUB", "USD", "EUR"]


class AccountResponse(BaseModel):
    id: str
    owner_name: str
    balance: int
    currency: str
