from datetime import datetime

from pydantic import BaseModel, ConfigDict

from corebank_api.schemas.common import Currency


class AccountCreateRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    currency: Currency


class AccountResponse(BaseModel):
    id: str
    user_id: str | None
    owner_name: str
    balance: int
    currency: str
    created_at: datetime
