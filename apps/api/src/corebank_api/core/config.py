from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    service_name: str = "corebank-api"
    version: str = "0.1.0"
    environment: str = "local"


settings = Settings()