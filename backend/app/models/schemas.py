from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.entities import ReviewPriority, ReviewStatus, SourceType


class LocationProvenance(StrEnum):
    USER_CONFIRMED = "USER_CONFIRMED"
    HUMAN_CONFIRMED = "HUMAN_CONFIRMED"
    UNKNOWN = "UNKNOWN"


class IncidentCreate(BaseModel):
    original_text: str = Field(default="", max_length=20_000)
    reporter_alias: str | None = Field(default=None, max_length=100)
    language_hint: str | None = Field(default=None, max_length=20)
    location_text: str | None = Field(default=None, max_length=500)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    location_provenance: LocationProvenance = LocationProvenance.UNKNOWN
    is_synthetic: bool = False

    @field_validator("original_text")
    @classmethod
    def trim_text(cls, value: str) -> str:
        return value.strip()


class IncidentUpdate(BaseModel):
    review_status: ReviewStatus | None = None
    review_priority: ReviewPriority | None = None
    human_notes: str | None = Field(default=None, max_length=10_000)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    location_provenance: LocationProvenance | None = None


class AnalysisLocation(BaseModel):
    place_name: str | None = None
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)


class GemmaAnalysisResult(BaseModel):
    detected_language: str | None = None
    english_translation: str | None = None
    short_summary: str = ""
    category: str | None = None
    reported_people_affected: int | None = Field(default=None, ge=0)
    reported_needs: list[str] = Field(default_factory=list)
    observable_image_details: list[str] = Field(default_factory=list)
    unverified_claims: list[str] = Field(default_factory=list)
    risk_signals: list[str] = Field(default_factory=list)
    location: AnalysisLocation = Field(default_factory=AnalysisLocation)
    follow_up_questions: list[str] = Field(default_factory=list)
    requires_human_review: bool = True


class MediaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    filename_sanitized: str
    mime_detected: str
    bytes: int
    sha256: str
    metadata_stripped: bool


class IncidentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    created_at: datetime
    updated_at: datetime
    reporter_alias: str | None
    language_hint: str | None
    original_text: str
    location_text: str | None
    latitude: float | None
    longitude: float | None
    location_provenance: str
    source_type: SourceType
    review_priority: ReviewPriority
    priority_reason: str | None
    review_status: ReviewStatus
    human_notes: str | None
    is_synthetic: bool
    revision: int
    media: list[MediaRead] = Field(default_factory=list)


class Envelope(BaseModel):
    data: object
    meta: dict[str, object] = Field(default_factory=dict)
    error: dict[str, object] | None = None
