from enum import StrEnum
from typing import Self

from pydantic import BaseModel, Field, model_validator

from corebank_api.schemas.common import Currency, Money


class TransferStatus(StrEnum):
    COMPLETED = "completed"


class TransferCreateRequest(BaseModel):
    from_account_id: str = Field(min_length=1)
    to_account_id: str | None = Field(default=None, min_length=1)
    recipient: str | None = Field(default=None, min_length=1, max_length=32)
    amount: Money = Field(gt=0)

    @model_validator(mode="after")
    def validate_destination(self) -> Self:
        if (self.to_account_id is None) == (self.recipient is None):
            raise ValueError("Provide exactly one of to_account_id or recipient")
        return self


class TransferResponse(BaseModel):
    transaction_id: str
    from_account_id: str
    to_account_id: str
    amount: Money
    status: TransferStatus


class RecipientLookupResponse(BaseModel):
    display_name: str
    masked_card_number: str
    currency: Currency
