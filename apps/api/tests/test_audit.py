import pytest
from corebank_api.database.models import AuditEventModel
from corebank_api.database.session import SessionLocal


def test_request_id_is_returned(client) -> None:
    response = client.get("/health", headers={"X-Request-ID": "request-test-123"})

    assert response.headers["X-Request-ID"] == "request-test-123"


@pytest.mark.db
def test_completed_transfer_creates_audit_event(auth_client) -> None:
    response = auth_client.post(
        "/transfers",
        json={"from_account_id": "acc-001", "to_account_id": "acc-002", "amount": "10.00"},
        headers={"X-Request-ID": "request-transfer-123"},
    )

    assert response.status_code == 201
    with SessionLocal() as session:
        event = session.query(AuditEventModel).one()
        assert event.event_type == "transfer.completed"
        assert event.entity_id == response.json()["transaction_id"]
        assert event.request_id == "request-transfer-123"
        assert event.details["amount"] == "10.00"
