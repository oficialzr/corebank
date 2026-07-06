from pydantic import BaseModel


class AccountCreateRequest(BaseModel):
    owner_name: str
    currency: str


class AccountResponse(BaseModel):
    id: str
    owner_name: str
    balance: int
    currency: str
