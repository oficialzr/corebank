from fastapi import APIRouter

from corebank_api.core.config import settings

router = APIRouter(tags=["System"])


@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/version")
def version() -> dict[str, str]:
    return {
        "service": settings.service_name,
        "version": settings.version,
        "environment": settings.environment,
    }
