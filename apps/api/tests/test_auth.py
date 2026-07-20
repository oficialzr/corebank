import pytest

pytestmark = pytest.mark.db


def registration_payload() -> dict[str, str]:
    return {
        "email": "Alex@Example.com",
        "password": "strong-password",
        "full_name": "Alex Ivanov",
        "phone_number": "+79991234567",
    }


def test_register_user_returns_created_user(client) -> None:
    response = client.post("/auth/register", json=registration_payload())

    assert response.status_code == 201

    user = response.json()

    assert user["id"].startswith("user-")
    assert user["email"] == "alex@example.com"
    assert user["full_name"] == "Alex Ivanov"
    assert user["phone_number"] == "+79991234567"
    assert user["is_active"] is True
    assert user["created_at"] is not None
    assert "password" not in user
    assert "password_hash" not in user


def test_register_user_rejects_duplicate_email(client) -> None:
    client.post("/auth/register", json=registration_payload())

    response = client.post("/auth/register", json=registration_payload())

    assert response.status_code == 409
    assert response.json() == {
        "detail": {
            "code": "email_already_registered",
            "message": "Email is already registered",
        }
    }


def test_register_user_rejects_short_password(client) -> None:
    payload = registration_payload()
    payload["password"] = "short"

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 422


def test_register_user_rejects_invalid_email(client) -> None:
    payload = registration_payload()
    payload["email"] = "not-an-email"

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 422


def test_register_user_normalizes_phone_number(client) -> None:
    payload = registration_payload()
    payload["phone_number"] = "8 (999) 123-45-67"

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 201
    assert response.json()["phone_number"] == "+79991234567"


def test_register_user_rejects_duplicate_phone(client) -> None:
    client.post("/auth/register", json=registration_payload())
    payload = registration_payload()
    payload["email"] = "another@example.com"

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 409
    assert response.json()["detail"]["code"] == "phone_already_registered"


def login_payload(password: str = "strong-password") -> dict[str, str]:
    return {
        "email": "alex@example.com",
        "password": password,
    }


def test_login_returns_access_token(client) -> None:
    client.post("/auth/register", json=registration_payload())

    response = client.post("/auth/login", json=login_payload())

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert response.json()["access_token"]


def test_login_rejects_invalid_credentials(client) -> None:
    client.post("/auth/register", json=registration_payload())

    response = client.post("/auth/login", json=login_payload(password="wrong-password"))

    assert response.status_code == 401
    assert response.json() == {
        "detail": {
            "code": "invalid_credentials",
            "message": "Invalid email or password",
        }
    }


def test_auth_me_returns_current_user(client) -> None:
    client.post("/auth/register", json=registration_payload())
    login_response = client.post("/auth/login", json=login_payload())
    access_token = login_response.json()["access_token"]

    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    assert response.json()["email"] == "alex@example.com"


def test_auth_me_rejects_invalid_token(client) -> None:
    response = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalid-token"},
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": {
            "code": "invalid_token",
            "message": "Invalid or expired access token",
        }
    }


def test_update_current_user_phone(auth_client) -> None:
    response = auth_client.patch(
        "/auth/me/phone",
        json={"phone_number": "8 (999) 555-44-33"},
    )

    assert response.status_code == 200
    assert response.json()["phone_number"] == "+79995554433"
