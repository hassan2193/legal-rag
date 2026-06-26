"""FastAPI application entry point."""

from fastapi import FastAPI

from src.api.routes import router

app = FastAPI(
    title="Legal Contract Extraction API",
)


@app.get("/")
def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "running"}


app.include_router(router)