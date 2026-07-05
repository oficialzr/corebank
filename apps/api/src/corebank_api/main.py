from fastapi import FastAPI

app = FastAPI(
    title="CoreBank API",
    version="0.1.0",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/version")
def version() -> dict[str, str]:
    return {
        "service": "corebank-api",
        "version": "0.1.0",
        "environment": "local",
    }