from pydantic import BaseModel


class AccountResponse(BaseModel):
    id: str
    owner_name: str
    balance: int
    currency: str
