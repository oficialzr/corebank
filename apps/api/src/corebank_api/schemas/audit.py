from datetime import datetime
from typing import Any

from pydantic import BaseModel


class AuditEventResponse(BaseModel):
    id: str
    user_id: str | None
    event_type: str
    entity_type: str | None
    entity_id: str | None
    request_id: str
    details: dict[str, Any]
    created_at: datetime


class AuditEventPage(BaseModel):
    items: list[AuditEventResponse]
    total: int
    limit: int
    offset: int
