"""Serialize ReviewResult to JSON."""

import json
from pathlib import Path

from pyreview.core.schemas import ReviewResult


def generate_json_report(
    result: ReviewResult,
    output_path: Path | None = None,
) -> str:
    """Produce a JSON report. Optionally write to file."""
    report = result.model_dump(mode="json")
    json_str = json.dumps(report, indent=2, default=str)
    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json_str, encoding="utf-8")
    return json_str
