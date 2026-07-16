import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    service_name: str
    version: str
    environment: str
    jwt_secret_key: str
    jwt_algorithm: str
    access_token_expire_minutes: int


def get_settings() -> Settings:
    return Settings(
        service_name=os.getenv("COREBANK_SERVICE_NAME", "corebank-api"),
        version=os.getenv("COREBANK_VERSION", "0.1.0"),
        environment=os.getenv("COREBANK_ENVIRONMENT", "local"),
        jwt_secret_key=os.getenv("COREBANK_JWT_SECRET_KEY", "corebank-dev-secret-key"),
        jwt_algorithm=os.getenv("COREBANK_JWT_ALGORITHM", "HS256"),
        access_token_expire_minutes=int(os.getenv("COREBANK_ACCESS_TOKEN_EXPIRE_MINUTES", "30")),
    )


settings = get_settings()
