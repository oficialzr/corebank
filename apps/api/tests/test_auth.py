def registration_payload() -> dict[str, str]:
    return {
        "email": "Alex@Example.com",
        "password": "strong-password",
        "full_name": "Alex Ivanov",
    }


def test_register_user_returns_created_user(client) -> None:
    response = client.post("/auth/register", json=registration_payload())

    assert response.status_code == 201

    user = response.json()

    assert user["id"].startswith("user-")
    assert user["email"] == "alex@example.com"
    assert user["full_name"] == "Alex Ivanov"
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