from __future__ import annotations

import hashlib
import io
from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status
from PIL import Image, UnidentifiedImageError

MAX_IMAGE_BYTES = 8 * 1024 * 1024
ALLOWED_MIME = {"image/jpeg", "image/png", "image/webp"}


@dataclass(frozen=True)
class StoredMedia:
    filename_sanitized: str
    mime_detected: str
    relative_path: str
    sha256: str
    bytes: int


def _detected_mime(image: Image.Image) -> str:
    return {"JPEG": "image/jpeg", "PNG": "image/png", "WEBP": "image/webp"}.get(
        image.format or "", ""
    )


async def store_image(upload: UploadFile, media_root: str, incident_id: str) -> StoredMedia:
    raw = await upload.read(MAX_IMAGE_BYTES + 1)
    if len(raw) > MAX_IMAGE_BYTES:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="Image exceeds 8 MB")
    if not raw:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Image is empty")
    try:
        image = Image.open(io.BytesIO(raw))
        image.verify()
        image = Image.open(io.BytesIO(raw))
    except (UnidentifiedImageError, OSError) as exc:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Invalid image") from exc

    mime = _detected_mime(image)
    if mime not in ALLOWED_MIME:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Only JPEG, PNG, and WebP are allowed")

    # Re-encode pixels so EXIF/GPS metadata is not retained.
    output = io.BytesIO()
    save_format = "JPEG" if mime == "image/jpeg" else image.format
    converted = image.convert("RGB") if save_format == "JPEG" else image
    converted.save(output, format=save_format, optimize=True)
    clean = output.getvalue()
    digest = hashlib.sha256(clean).hexdigest()
    extension = "jpg" if save_format == "JPEG" else save_format.lower()
    filename = f"{uuid4().hex}.{extension}"
    relative = Path(incident_id) / filename
    destination = Path(media_root) / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(clean)
    return StoredMedia(filename, mime, relative.as_posix(), digest, len(clean))
