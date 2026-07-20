from datetime import datetime

from pydantic import BaseModel

from corebank_api.schemas.common import Currency, Money
from corebank_api.schemas.transfer import TransferStatus


class TransactionResponse(BaseModel):
    id: str
    from_account_id: str
    to_account_id: str
    from_account: str | None = None
    to_account: str | None = None
    amount: Money
    currency: Currency
    status: TransferStatus
    created_at: datetime
