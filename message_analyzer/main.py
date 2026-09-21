"""Entry point for the Phase 2 message analysis service."""

from fastapi import FastAPI


app = FastAPI(title="Guest Message Analyzer")


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Report that the HTTP service is running."""
    return {"status": "ok"}
