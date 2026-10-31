from datetime import UTC, datetime

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.evaluation import router as evaluation_router
from app.api.reports import router as reports_router
from app.core.config import get_settings
from app.core.db import init_db

settings = get_settings()
app = FastAPI(title="RescueBridge AI API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH", "OPTIONS"],
    allow_headers=["Content-Type"],
)
app.include_router(reports_router)
app.include_router(evaluation_router)


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/")
async def root() -> dict[str, object]:
    """Provide a useful landing response for the backend port."""
    return {
        "service": "RescueBridge AI API",
        "status": "ok",
        "runtime_location": "HOSTED" if settings.ai_mode == "hosted_gemma" else "LOCAL",
        "api_health": "/api/v1/health",
        "runtime_settings": "/api/v1/settings/runtime",
        "frontend": "http://127.0.0.1:5173/",
    }


@app.get("/api/v1/health")
async def health() -> dict[str, object]:
    """Return runtime status without exposing secrets."""
    runtime_location = "HOSTED" if settings.ai_mode == "hosted_gemma" else "LOCAL"
    ollama_status = "NOT_CONFIGURED"
    ollama_error: str | None = None
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            response = await client.get(f"{settings.ollama_base_url}/api/tags")
            response.raise_for_status()
            models = response.json().get("models", [])
            names = {item.get("name") for item in models if isinstance(item, dict)}
            ollama_status = "LIVE" if settings.local_model in names else "MODEL_NOT_VERIFIED"
    except (httpx.HTTPError, ValueError) as exc:
        ollama_status = "UNAVAILABLE"
        ollama_error = type(exc).__name__

    return {
        "data": {
            "service": "ok",
            "ai_mode": settings.ai_mode,
            "runtime_location": runtime_location,
            "active_provider": "gemini_hosted_evaluation" if runtime_location == "HOSTED" else "ollama_local",
            "active_model": settings.hosted_model if runtime_location == "HOSTED" else settings.local_model,
            "local_provider": {
                "model": settings.local_model,
                "status": ollama_status,
                "error": ollama_error,
                "used_for_current_requests": runtime_location == "LOCAL",
            },
            "hosted_evaluation": {
                "status": "READY" if settings.allow_hosted_evaluation and settings.gemini_api_key else "NOT_CONFIGURED",
                "model": settings.hosted_model,
                "used_for_current_requests": runtime_location == "HOSTED",
            },
            "checked_at": datetime.now(UTC).isoformat(),
        },
        "meta": {"runtime_location": runtime_location},
        "error": None,
    }


@app.get("/api/v1/settings/runtime")
async def runtime_settings() -> dict[str, object]:
    runtime_location = "HOSTED" if settings.ai_mode == "hosted_gemma" else "LOCAL"
    return {
        "data": {
            "ai_mode": settings.ai_mode,
            "runtime_location": runtime_location,
            "active_provider": "gemini_hosted_evaluation" if runtime_location == "HOSTED" else "ollama_local",
            "active_model": settings.hosted_model if runtime_location == "HOSTED" else settings.local_model,
            "configured_local_model": settings.local_model,
            "ollama_base_url": settings.ollama_base_url,
            "allow_hosted_evaluation": settings.allow_hosted_evaluation,
            "hosted_model": settings.hosted_model,
            "hosted_api_configured": bool(settings.gemini_api_key),
        },
        "meta": {"runtime_location": runtime_location},
        "error": None,
    }
