"""FastAPI application entrypoint for OORCA."""

from __future__ import annotations

from fastapi import FastAPI

from backend.api.routes import (
    attribution,
    detections,
    ecology,
    forecasts,
    liability,
    vessels,
)


def create_app() -> FastAPI:
    app = FastAPI(
        title="OORCA API",
        description="Ocean Oil Spill Response, Attribution & Compensation Analytics",
        version="0.1.0",
    )

    app.include_router(detections.router, prefix="/api/detections", tags=["detections"])
    app.include_router(vessels.router, prefix="/api/vessels", tags=["vessels"])
    app.include_router(attribution.router, prefix="/api/attribution", tags=["attribution"])
    app.include_router(forecasts.router, prefix="/api/forecasts", tags=["forecasts"])
    app.include_router(ecology.router, prefix="/api/ecology", tags=["ecology"])
    app.include_router(liability.router, prefix="/api/liability", tags=["liability"])

    @app.get("/health", tags=["meta"])
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()