from fastapi import APIRouter

router = APIRouter(tags=["service"])


@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/version")
def version() -> dict[str, str]:
    return {
        "service": "corebank-api",
        "version": "0.1.0",
        "environment": "local",
    }