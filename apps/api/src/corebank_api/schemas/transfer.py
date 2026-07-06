from enum import StrEnum

from pydantic import BaseModel, Field


class TransferStatus(StrEnum):
    COMPLETED = "completed"


class TransferCreateRequest(BaseModel):
    from_account_id: str = Field(min_length=1)
    to_account_id: str = Field(min_length=1)
    amount: int = Field(gt=0)


class TransferResponse(BaseModel):
    from_account_id: str
    to_account_id: str
    amount: int
    status: TransferStatus