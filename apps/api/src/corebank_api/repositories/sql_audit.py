from datetime import datetime

from sqlalchemy.orm import Session

from corebank_api.database.models import AuditEventModel
from corebank_api.schemas.audit import AuditEventPage, AuditEventResponse


def model_to_schema(event: AuditEventModel) -> AuditEventResponse:
    return AuditEventResponse(
        id=event.id,
        user_id=event.user_id,
        event_type=event.event_type,
        entity_type=event.entity_type,
        entity_id=event.entity_id,
        request_id=event.request_id,
        details=event.details,
        created_at=event.created_at,
    )


def list_audit_events(
    session: Session,
    *,
    user_id: str | None = None,
    event_type: str | None = None,
    request_id: str | None = None,
    created_from: datetime | None = None,
    created_to: datetime | None = None,
    limit: int = 50,
    offset: int = 0,
) -> AuditEventPage:
    query = session.query(AuditEventModel)
    if user_id is not None:
        query = query.filter(AuditEventModel.user_id == user_id)
    if event_type is not None:
        query = query.filter(AuditEventModel.event_type == event_type)
    if request_id is not None:
        query = query.filter(AuditEventModel.request_id == request_id)
    if created_from is not None:
        query = query.filter(AuditEventModel.created_at >= created_from)
    if created_to is not None:
        query = query.filter(AuditEventModel.created_at <= created_to)

    total = query.count()
    events = query.order_by(AuditEventModel.created_at.desc()).limit(limit).offset(offset).all()
    return AuditEventPage(
        items=[model_to_schema(event) for event in events],
        total=total,
        limit=limit,
        offset=offset,
    )
