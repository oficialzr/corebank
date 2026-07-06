from fastapi import FastAPI

from corebank_api.api.accounts import router as accounts_router
from corebank_api.api.health import router as health_router
from corebank_api.api.transfers import router as transfers_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="CoreBank API",
        version="0.1.0",
    )

    app.include_router(health_router)
    app.include_router(accounts_router)
    app.include_router(transfers_router)

    return app


app = create_app()
