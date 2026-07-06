from datetime import datetime

from pydantic import BaseModel

from corebank_api.schemas.common import Currency
from corebank_api.schemas.transfer import TransferStatus


class TransactionResponse(BaseModel):
    id: str
    from_account_id: str
    to_account_id: str
    amount: int
    currency: Currency
    status: TransferStatus
    created_at: datetime
