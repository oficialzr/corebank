from corebank_api.core.config import get_settings


def test_get_settings_uses_default_values(monkeypatch) -> None:
    monkeypatch.delenv("COREBANK_SERVICE_NAME", raising=False)
    monkeypatch.delenv("COREBANK_VERSION", raising=False)
    monkeypatch.delenv("COREBANK_ENVIRONMENT", raising=False)
    monkeypatch.delenv("COREBANK_REPOSITORY_BACKEND", raising=False)

    settings = get_settings()

    assert settings.repository_backend == "memory"
    assert settings.service_name == "corebank-api"
    assert settings.version == "0.1.0"
    assert settings.environment == "local"


def test_get_settings_reads_environment_variables(monkeypatch) -> None:
    monkeypatch.setenv("COREBANK_SERVICE_NAME", "test-service")
    monkeypatch.setenv("COREBANK_VERSION", "9.9.9")
    monkeypatch.setenv("COREBANK_ENVIRONMENT", "test")
    monkeypatch.setenv("COREBANK_REPOSITORY_BACKEND", "sql")

    settings = get_settings()

    assert settings.repository_backend == "sql"
    assert settings.service_name == "test-service"
    assert settings.version == "9.9.9"
    assert settings.environment == "test"
