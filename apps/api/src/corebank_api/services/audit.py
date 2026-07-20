from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy.orm import Session

from corebank_api.core.request_context import get_request_id
from corebank_api.database.models import AuditEventModel
from corebank_api.database.session import SessionLocal
from corebank_api.repositories.sql_audit import list_audit_events as query_audit_events
from corebank_api.schemas.audit import AuditEventPage


def append_audit_event(
    event_type: str,
    *,
    user_id: str | None = None,
    entity_type: str | None = None,
    entity_id: str | None = None,
    details: dict | None = None,
    session: Session | None = None,
) -> AuditEventModel:
    event = AuditEventModel(
        id=f"audit-{uuid4()}",
        user_id=user_id,
        event_type=event_type,
        entity_type=entity_type,
        entity_id=entity_id,
        request_id=get_request_id(),
        details=details or {},
        created_at=datetime.now(UTC),
    )

    if session is not None:
        session.add(event)
        return event

    with SessionLocal() as own_session:
        own_session.add(event)
        own_session.commit()
        own_session.refresh(event)
        return event


def list_audit_events(**filters) -> AuditEventPage:
    with SessionLocal() as session:
        return query_audit_events(session, **filters)
