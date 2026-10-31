from __future__ import annotations

import json
from dataclasses import dataclass

from app.core.config import get_settings
from app.models.schemas import GemmaAnalysisResult


class HostedGemmaError(RuntimeError):
    """A safe, user-facing hosted Gemma failure."""


@dataclass(frozen=True)
class HostedGemmaResult:
    analysis: GemmaAnalysisResult
    model: str
    runtime_location: str = "HOSTED"


SYSTEM_PROMPT = """You are a human-supervised disaster report extraction assistant.
Return JSON only. Preserve the original language and distinguish reported facts,
observable image details, and unverified inferences. Never invent coordinates,
casualty counts, structural safety, route safety, or supply availability.
The input is synthetic evaluation data. Output must match the requested schema.
"""


def _client():
    settings = get_settings()
    if not settings.allow_hosted_evaluation:
        raise HostedGemmaError("Hosted Gemma evaluation is disabled")
    if not settings.gemini_api_key:
        raise HostedGemmaError("GEMINI_API_KEY is not configured")
    try:
        from google import genai
    except ImportError as exc:
        raise HostedGemmaError("Install the google-genai package") from exc
    return genai.Client(api_key=settings.gemini_api_key)


def _parse(text: str) -> GemmaAnalysisResult:
    try:
        candidate = text.strip()
        if candidate.startswith("```"):
            candidate = candidate.split("\n", 1)[1] if "\n" in candidate else candidate
            if candidate.endswith("```"):
                candidate = candidate[:-3].rstrip()
        # Hosted models sometimes add a short preamble around an otherwise
        # valid object. Keep parsing constrained to the first JSON object.
        start = candidate.find("{")
        end = candidate.rfind("}")
        if start >= 0 and end > start:
            candidate = candidate[start : end + 1]
        payload = json.loads(candidate)
        return GemmaAnalysisResult.model_validate(payload)
    except (json.JSONDecodeError, TypeError, ValueError) as exc:
        raise HostedGemmaError("Hosted Gemma returned invalid JSON") from exc


def analyze_synthetic_report(
    original_text: str,
    image_bytes: bytes | None = None,
    image_mime: str | None = None,
) -> HostedGemmaResult:
    """Run the explicit hosted evaluation path on synthetic content only."""
    settings = get_settings()
    client = _client()
    schema = json.dumps(GemmaAnalysisResult.model_json_schema(), ensure_ascii=False)
    prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"Required JSON schema:\n{schema}\n\n"
        f"Report text:\n{original_text}\n\n"
        "Populate every schema field when the report supports it; use null or [] "
        "when unknown. Return only one JSON object, with no markdown fences."
    )
    contents: list[object] = [prompt]
    if image_bytes:
        if image_mime not in {"image/jpeg", "image/png", "image/webp"}:
            raise HostedGemmaError("Image MIME must be JPEG, PNG, or WebP")
        from google.genai import types

        contents.insert(0, types.Part.from_bytes(data=image_bytes, mime_type=image_mime))
    try:
        response = client.models.generate_content(
            model=settings.hosted_model,
            contents=contents,
        )
    except Exception as exc:  # SDK exceptions vary across releases; do not expose details.
        raise HostedGemmaError("Hosted Gemma request failed") from exc
    response_text = getattr(response, "text", None)
    if not response_text:
        raise HostedGemmaError("Hosted Gemma returned an empty response")
    return HostedGemmaResult(analysis=_parse(response_text), model=settings.hosted_model)
