import base64
import binascii

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.services.gemini_hosted import HostedGemmaError, analyze_synthetic_report

router = APIRouter(prefix="/api/v1/evaluation/gemini", tags=["hosted-evaluation"])


class HostedEvaluationRequest(BaseModel):
    is_synthetic: bool = False
    original_text: str = Field(min_length=1, max_length=20_000)
    image_base64: str | None = None
    image_mime: str | None = None


@router.post("/analyze")
def hosted_analysis(request: HostedEvaluationRequest) -> dict[str, object]:
    if not request.is_synthetic:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Hosted evaluation accepts synthetic data only",
        )
    image_bytes = None
    if request.image_base64:
        try:
            image_bytes = base64.b64decode(request.image_base64, validate=True)
        except (binascii.Error, ValueError) as exc:
            raise HTTPException(status_code=422, detail="image_base64 is invalid") from exc
    try:
        result = analyze_synthetic_report(request.original_text, image_bytes, request.image_mime)
    except HostedGemmaError as exc:
        raise HTTPException(status_code=412, detail=str(exc)) from exc
    return {
        "data": result.analysis,
        "meta": {
            "provider": "gemini_hosted_evaluation",
            "model": result.model,
            "runtime_location": result.runtime_location,
            "data_policy": "SYNTHETIC_ONLY",
        },
        "error": None,
    }
