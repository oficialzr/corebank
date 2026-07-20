from datetime import datetime

from fastapi import APIRouter, Query

from corebank_api.api.auth import AdminUser
from corebank_api.schemas.audit import AuditEventPage
from corebank_api.services.audit import list_audit_events

router = APIRouter(prefix="/admin/audit-events", tags=["Admin audit"])


@router.get("", response_model=AuditEventPage)
def list_audit_events_endpoint(
    _: AdminUser,
    user_id: str | None = Query(default=None, min_length=1),
    event_type: str | None = Query(default=None, min_length=1, max_length=64),
    request_id: str | None = Query(default=None, min_length=1, max_length=64),
    created_from: datetime | None = None,
    created_to: datetime | None = None,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> AuditEventPage:
    return list_audit_events(
        user_id=user_id,
        event_type=event_type,
        request_id=request_id,
        created_from=created_from,
        created_to=created_to,
        limit=limit,
        offset=offset,
    )
