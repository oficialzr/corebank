from corebank_api.core.config import get_settings


def test_get_settings_uses_default_values(monkeypatch) -> None:
    monkeypatch.delenv("COREBANK_SERVICE_NAME", raising=False)
    monkeypatch.delenv("COREBANK_VERSION", raising=False)
    monkeypatch.delenv("COREBANK_ENVIRONMENT", raising=False)
    monkeypatch.delenv("COREBANK_JWT_SECRET_KEY", raising=False)
    monkeypatch.delenv("COREBANK_JWT_ALGORITHM", raising=False)
    monkeypatch.delenv("COREBANK_ACCESS_TOKEN_EXPIRE_MINUTES", raising=False)

    settings = get_settings()

    assert settings.service_name == "corebank-api"
    assert settings.version == "0.1.0"
    assert settings.environment == "local"
    assert settings.jwt_secret_key == "corebank-dev-secret-key"
    assert settings.jwt_algorithm == "HS256"
    assert settings.access_token_expire_minutes == 30


def test_get_settings_reads_environment_variables(monkeypatch) -> None:
    monkeypatch.setenv("COREBANK_SERVICE_NAME", "test-service")
    monkeypatch.setenv("COREBANK_VERSION", "9.9.9")
    monkeypatch.setenv("COREBANK_ENVIRONMENT", "test")
    monkeypatch.setenv("COREBANK_JWT_SECRET_KEY", "super-secret")
    monkeypatch.setenv("COREBANK_JWT_ALGORITHM", "HS256")
    monkeypatch.setenv("COREBANK_ACCESS_TOKEN_EXPIRE_MINUTES", "15")

    settings = get_settings()

    assert settings.service_name == "test-service"
    assert settings.version == "9.9.9"
    assert settings.environment == "test"
    assert settings.jwt_secret_key == "super-secret"
    assert settings.jwt_algorithm == "HS256"
    assert settings.access_token_expire_minutes == 15
