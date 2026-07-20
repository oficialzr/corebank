import logging
from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI, Request

from corebank_api.api.accounts import router as accounts_router
from corebank_api.api.admin_audit import router as admin_audit_router
from corebank_api.api.auth import router as auth_router
from corebank_api.api.health import router as health_router
from corebank_api.api.transactions import router as transactions_router
from corebank_api.api.transfers import router as transfers_router
from corebank_api.core.logging import configure_logging
from corebank_api.core.request_context import request_id_context


def create_app() -> FastAPI:
    configure_logging()
    request_logger = logging.getLogger("corebank.request")
    app = FastAPI(
        title="CoreBank API",
        description="Production-like banking backend API built with FastAPI, PostgreSQL, Docker, Alembic, and CI.",
        version="0.1.0",
    )

    @app.middleware("http")
    async def attach_request_id(request: Request, call_next):
        request_id = request.headers.get("X-Request-ID") or str(uuid4())
        token = request_id_context.set(request_id)
        started_at = perf_counter()
        try:
            response = await call_next(request)
            response.headers["X-Request-ID"] = request_id
            request_logger.info(
                "request.completed",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "duration_ms": round((perf_counter() - started_at) * 1000, 2),
                },
            )
            return response
        except Exception:
            request_logger.exception(
                "request.failed",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": 500,
                    "duration_ms": round((perf_counter() - started_at) * 1000, 2),
                },
            )
            raise
        finally:
            request_id_context.reset(token)

    app.include_router(health_router)
    app.include_router(auth_router)
    app.include_router(accounts_router)
    app.include_router(admin_audit_router)
    app.include_router(transfers_router)
    app.include_router(transactions_router)

    return app


app = create_app()
