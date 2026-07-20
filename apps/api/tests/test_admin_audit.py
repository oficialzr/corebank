import pytest

pytestmark = pytest.mark.db


def create_audited_transfer(auth_client, request_id: str = "audit-filter-request") -> str:
    response = auth_client.post(
        "/transfers",
        json={"from_account_id": "acc-001", "to_account_id": "acc-002", "amount": "10.00"},
        headers={"X-Request-ID": request_id},
    )
    assert response.status_code == 201
    return response.json()["transaction_id"]


def test_admin_can_filter_audit_events(auth_client) -> None:
    transaction_id = create_audited_transfer(auth_client)

    response = auth_client.get(
        "/admin/audit-events",
        params={"event_type": "transfer.completed", "request_id": "audit-filter-request"},
    )

    assert response.status_code == 200
    page = response.json()
    assert page["total"] == 1
    assert page["limit"] == 50
    assert page["offset"] == 0
    assert page["items"][0]["entity_id"] == transaction_id
    assert page["items"][0]["details"]["amount"] == "10.00"


def test_non_admin_cannot_read_audit_events(maria_auth_client) -> None:
    response = maria_auth_client.get("/admin/audit-events")

    assert response.status_code == 403
    assert response.json()["detail"]["code"] == "admin_access_required"


def test_audit_events_endpoint_requires_authentication(client) -> None:
    response = client.get("/admin/audit-events")

    assert response.status_code == 401
