"""Entry point for the Phase 2 message analysis service."""

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI

from database import initialize_database


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Initialize local resources before accepting requests."""
    initialize_database()
    yield


app = FastAPI(title="Guest Message Analyzer", lifespan=lifespan)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Report that the HTTP service is running."""
    return {"status": "ok"}
