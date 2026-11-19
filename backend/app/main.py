"""First-slice API: one form, one fixture album, local selection only (M1-01).

Contract:
- GET /healthz returns {"status": "ok"} without touching any provider.
- POST /api/recommendations accepts {"description": str, "recent_ids": [str]}
  and returns {"album": {...}, "mode": "local"} from the synthetic fixture.

Validation (P01): the description is trimmed and must hold 1-500
characters. Invalid input returns 422 and never reaches selection.
Privacy (P08): full descriptions and raw provider payloads stay out of
logs and stored data. Logs carry timestamp, request ID, route, status,
elapsed time, selection mode and a safe provider outcome only.
Health (operations): /healthz reflects local readiness only.

The built frontend in frontend/dist is served from the same origin when
present, so the release image keeps one service for the page and the API.
"""

from __future__ import annotations

import logging
import time
import uuid
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator

from .fixture import FIXTURE_ALBUMS, select_album

logger = logging.getLogger("jazzy_mood")

MAX_DESCRIPTION = 500
MAX_RECENT_IDS = 20


class RecommendationRequest(BaseModel):
    description: str
    recent_ids: list[str] = Field(default_factory=list)

    @field_validator("description")
    @classmethod
    def description_must_be_usable(cls, value: str) -> str:
        trimmed = value.strip()
        if not trimmed:
            raise ValueError("Please describe what you want to hear.")
        if len(trimmed) > MAX_DESCRIPTION:
            raise ValueError("Please keep your description to 500 characters or fewer.")
        return trimmed

    @field_validator("recent_ids")
    @classmethod
    def recent_ids_must_be_bounded(cls, value: list[str]) -> list[str]:
        if len(value) > MAX_RECENT_IDS:
            raise ValueError("Too many recent IDs; send 20 or fewer.")
        cleaned = [item.strip() for item in value if isinstance(item, str) and item.strip()]
        if len(cleaned) != len(value):
            raise ValueError("Recent IDs must be nonblank strings.")
        return cleaned


class Album(BaseModel):
    id: str
    artist: str
    title: str
    year: int | None = None
    listening_url: str
    listening_label: str
    reason: str
    tag_status: str


class RecommendationResponse(BaseModel):
    album: Album
    mode: str = "local"


app = FastAPI(title="Jazzy Mood (M1 slice)")


@app.middleware("http")
async def request_context(request: Request, call_next):
    request_id = uuid.uuid4().hex[:12]
    request.state.request_id = request_id
    started = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception:
        elapsed_ms = int((time.perf_counter() - started) * 1000)
        # Log even when the handler fails so the request stays traceable.
        logger.exception(
            "request request_id=%s route=%s method=%s status=error elapsed_ms=%s",
            request_id,
            request.url.path,
            request.method,
            elapsed_ms,
        )
        raise
    elapsed_ms = int((time.perf_counter() - started) * 1000)
    # Never log the description, query string or body. Route path only.
    logger.info(
        "request request_id=%s route=%s method=%s status=%s elapsed_ms=%s",
        request_id,
        request.url.path,
        request.method,
        response.status_code,
        elapsed_ms,
    )
    response.headers["X-Request-ID"] = request_id
    return response


@app.get("/healthz")
def healthz():
    """Cheap local readiness check. No provider contact. P07, operations."""
    ready = bool(FIXTURE_ALBUMS)
    if not ready:
        return JSONResponse(status_code=503, content={"status": "not ready"})
    return {"status": "ok"}


@app.post("/api/recommendations", response_model=RecommendationResponse)
def recommend(payload: RecommendationRequest, request: Request):
    request_id = getattr(request.state, "request_id", "-")
    album = select_album(payload.recent_ids)
    # Structured event without visitor text. P08: description never logged.
    logger.info(
        "recommendation request_id=%s mode=local provider_outcome=disabled album_id=%s",
        request_id,
        album["id"],
    )
    return {"album": album, "mode": "local"}


def _frontend_dist() -> Path | None:
    root = Path(__file__).resolve().parents[2]
    dist = root / "frontend" / "dist"
    if dist.is_dir() and (dist / "index.html").exists():
        return dist
    return None


_dist = _frontend_dist()
if _dist is not None:  # pragma: no cover - exercised in production image and e2e
    app.mount("/", StaticFiles(directory=str(_dist), html=True), name="frontend")
else:  # pragma: no cover - local API-only development without a frontend build

    @app.get("/")
    def api_only() -> dict:
        return {"message": "Jazzy Mood API. Build the frontend for the full page."}
