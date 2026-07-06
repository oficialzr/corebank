from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class AccountCreateRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    
    owner_name: str = Field(min_length=1)
    currency: Literal["RUB", "USD", "EUR"]


class AccountResponse(BaseModel):
    id: str
    owner_name: str
    balance: int
    currency: str
