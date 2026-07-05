import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    service_name: str
    version: str
    environment: str


def get_settings() -> Settings:
    return Settings(
        service_name=os.getenv("COREBANK_SERVICE_NAME", "corebank-api"),
        version=os.getenv("COREBANK_VERSION", "0.1.0"),
        environment=os.getenv("COREBANK_ENVIRONMENT", "local"),
    )


settings = get_settings()