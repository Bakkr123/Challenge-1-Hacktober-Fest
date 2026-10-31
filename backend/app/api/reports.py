from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.config import get_settings
from app.core.db import get_db
from app.models.entities import Incident, Media, SourceType
from app.models.schemas import IncidentRead, IncidentUpdate
from app.services.media import store_image

router = APIRouter(prefix="/api/v1", tags=["incidents"])
settings = get_settings()


def _read(incident: Incident) -> IncidentRead:
    return IncidentRead.model_validate(incident)


@router.post("/reports", status_code=status.HTTP_201_CREATED)
async def create_report(
    original_text: str = Form(default=""),
    reporter_alias: str | None = Form(default=None),
    language_hint: str | None = Form(default=None),
    location_text: str | None = Form(default=None),
    latitude: float | None = Form(default=None),
    longitude: float | None = Form(default=None),
    image: UploadFile | None = File(default=None),
    is_synthetic: bool = Form(default=False),
    db: Session = Depends(get_db),
) -> dict[str, object]:
    original_text = original_text.strip()
    if not original_text and image is None:
        raise HTTPException(status_code=422, detail="Provide report text or an image")
    if (latitude is None) != (longitude is None):
        raise HTTPException(status_code=422, detail="Latitude and longitude must be provided together")

    incident = Incident(
        original_text=original_text,
        reporter_alias=reporter_alias,
        language_hint=language_hint,
        location_text=location_text,
        latitude=latitude,
        longitude=longitude,
        location_provenance="USER_CONFIRMED" if latitude is not None else "UNKNOWN",
        source_type=SourceType.TEXT_AND_IMAGE if image and original_text else SourceType.IMAGE if image else SourceType.TEXT,
        is_synthetic=is_synthetic,
    )
    db.add(incident)
    db.flush()
    if image:
        stored = await store_image(image, settings.media_root, incident.id)
        db.add(Media(
            incident_id=incident.id,
            filename_sanitized=stored.filename_sanitized,
            mime_detected=stored.mime_detected,
            storage_relative_path=stored.relative_path,
            sha256=stored.sha256,
            bytes=stored.bytes,
            metadata_stripped=True,
        ))
    db.commit()
    db.refresh(incident)
    return {"data": _read(incident), "meta": {"analysis": "NOT_STARTED"}, "error": None}


@router.get("/incidents", response_model=dict)
def list_incidents(db: Session = Depends(get_db)) -> dict[str, object]:
    incidents = db.scalars(select(Incident).options(selectinload(Incident.media)).order_by(Incident.created_at.desc())).all()
    return {"data": [IncidentRead.model_validate(item) for item in incidents], "meta": {}, "error": None}


@router.get("/incidents/{incident_id}", response_model=dict)
def get_incident(incident_id: str, db: Session = Depends(get_db)) -> dict[str, object]:
    incident = db.scalar(select(Incident).options(selectinload(Incident.media)).where(Incident.id == incident_id))
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    return {"data": _read(incident), "meta": {}, "error": None}


@router.patch("/incidents/{incident_id}", response_model=dict)
def update_incident(incident_id: str, update: IncidentUpdate, db: Session = Depends(get_db)) -> dict[str, object]:
    incident = db.get(Incident, incident_id)
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    for field, value in update.model_dump(exclude_unset=True).items():
        setattr(incident, field, value)
    incident.revision += 1
    db.commit()
    db.refresh(incident)
    return {"data": _read(incident), "meta": {"updated_by": "LOCAL_USER"}, "error": None}
