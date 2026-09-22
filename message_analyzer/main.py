"""Entry point for the Phase 2 message analysis service."""

from fastapi import FastAPI

from schemas import MessageRequest


app = FastAPI(title="Guest Message Analyzer")


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Report that the HTTP service is running."""
    return {"status": "ok"}


@app.post("/messages")
async def validate_message(_message: MessageRequest) -> dict[str, str]:
    """Validate a message received from Phase 1 before it is persisted."""
    return {"status": "validated"}
