"""Run the hosted Gemma evaluation adapter with synthetic data only.

Usage:
  PYTHONPATH=backend .venv/bin/python integrations/gemini_demo/run.py
"""

import json
import os
from pathlib import Path

from app.services.gemini_hosted import HostedGemmaError, analyze_synthetic_report


def main() -> int:
    text = os.getenv(
        "DEMO_TEXT",
        "ہمارے گاؤں کے پل کو سیلاب سے نقصان پہنچا ہے۔ بیس لوگ پھنسے ہوئے ہیں۔",
    )
    image_path = os.getenv("DEMO_IMAGE")
    image_bytes = Path(image_path).read_bytes() if image_path else None
    mime = "image/jpeg" if image_path and image_path.lower().endswith((".jpg", ".jpeg")) else "image/png"
    try:
        result = analyze_synthetic_report(text, image_bytes, mime if image_bytes else None)
    except HostedGemmaError as exc:
        print(json.dumps({"status": "NOT_CONFIGURED", "error": str(exc)}))
        return 2
    print(json.dumps({"status": "LIVE", "model": result.model, "analysis": result.analysis.model_dump()}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
