from datetime import UTC, datetime
from enum import StrEnum
from uuid import uuid4

from sqlalchemy import JSON, Boolean, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


def utc_now() -> datetime:
    return datetime.now(UTC)


class SourceType(StrEnum):
    TEXT = "TEXT"
    IMAGE = "IMAGE"
    TEXT_AND_IMAGE = "TEXT_AND_IMAGE"
    AUDIO = "AUDIO"


class ReviewStatus(StrEnum):
    UNREVIEWED = "UNREVIEWED"
    IN_REVIEW = "IN_REVIEW"
    VERIFIED_BY_HUMAN = "VERIFIED_BY_HUMAN"
    NEEDS_MORE_INFO = "NEEDS_MORE_INFO"
    CLOSED = "CLOSED"


class ReviewPriority(StrEnum):
    CRITICAL_REVIEW = "CRITICAL_REVIEW"
    HIGH_REVIEW = "HIGH_REVIEW"
    NORMAL_REVIEW = "NORMAL_REVIEW"
    UNKNOWN = "UNKNOWN"


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)
    reporter_alias: Mapped[str | None] = mapped_column(String(100), nullable=True)
    language_hint: Mapped[str | None] = mapped_column(String(20), nullable=True)
    original_text: Mapped[str] = mapped_column(Text, default="")
    location_text: Mapped[str | None] = mapped_column(String(500), nullable=True)
    latitude: Mapped[float | None] = mapped_column(nullable=True)
    longitude: Mapped[float | None] = mapped_column(nullable=True)
    location_provenance: Mapped[str] = mapped_column(String(30), default="UNKNOWN")
    source_type: Mapped[SourceType] = mapped_column(Enum(SourceType), default=SourceType.TEXT)
    review_priority: Mapped[ReviewPriority] = mapped_column(Enum(ReviewPriority), default=ReviewPriority.UNKNOWN)
    priority_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    review_status: Mapped[ReviewStatus] = mapped_column(Enum(ReviewStatus), default=ReviewStatus.UNREVIEWED)
    human_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_synthetic: Mapped[bool] = mapped_column(Boolean, default=False)
    revision: Mapped[int] = mapped_column(Integer, default=1)

    media: Mapped[list["Media"]] = relationship(back_populates="incident", cascade="all, delete-orphan")
    analyses: Mapped[list["AIAnalysis"]] = relationship(back_populates="incident", cascade="all, delete-orphan")


class Media(Base):
    __tablename__ = "media"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    incident_id: Mapped[str] = mapped_column(ForeignKey("incidents.id", ondelete="CASCADE"))
    filename_sanitized: Mapped[str] = mapped_column(String(255))
    mime_detected: Mapped[str] = mapped_column(String(100))
    storage_relative_path: Mapped[str] = mapped_column(String(500))
    sha256: Mapped[str] = mapped_column(String(64))
    bytes: Mapped[int] = mapped_column(Integer)
    metadata_stripped: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    incident: Mapped[Incident] = relationship(back_populates="media")


class AIAnalysis(Base):
    __tablename__ = "ai_analyses"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    incident_id: Mapped[str] = mapped_column(ForeignKey("incidents.id", ondelete="CASCADE"))
    provider: Mapped[str] = mapped_column(String(50))
    model_identifier: Mapped[str] = mapped_column(String(100))
    runtime_location: Mapped[str] = mapped_column(String(20))
    prompt_version: Mapped[str] = mapped_column(String(50))
    result_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    error_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    duration_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    reviewed_by_human: Mapped[bool] = mapped_column(Boolean, default=False)

    incident: Mapped[Incident] = relationship(back_populates="analyses")


class OutboxAction(Base):
    __tablename__ = "outbox_actions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    kind: Mapped[str] = mapped_column(String(100))
    payload_redacted: Mapped[dict] = mapped_column(JSON, default=dict)
    idempotency_key: Mapped[str] = mapped_column(String(100), unique=True)
    state: Mapped[str] = mapped_column(String(30), default="QUEUED")
    attempt_count: Mapped[int] = mapped_column(Integer, default=0)
    last_error_sanitized: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)


class AuditEvent(Base):
    __tablename__ = "audit_events"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    incident_id: Mapped[str | None] = mapped_column(ForeignKey("incidents.id", ondelete="SET NULL"), nullable=True)
    actor_type: Mapped[str] = mapped_column(String(30))
    action: Mapped[str] = mapped_column(String(100))
    old_value_redacted: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    new_value_redacted: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
