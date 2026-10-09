"""Entry point for the Phase 2 message analysis service."""

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from database import check_duplication, save_message
from schemas import MessageRequest


app = FastAPI(title="Guest Message Analyzer")


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Report that the HTTP service is running."""
    return {"status": "ok"}


@app.post("/messages", status_code=201)
async def save_received_message(message: MessageRequest):
    """Save a validated message received from Phase 1."""
    if check_duplication(message):
        return JSONResponse(status_code=200, content={"status": "duplicate"})

    save_message(message)
    return {"status": "saved"}
