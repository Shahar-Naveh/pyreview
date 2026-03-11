"""Load Python files from local paths or directories."""

from __future__ import annotations

from pathlib import Path

from pyreview.core.config import Settings
from pyreview.core.constants import SKIP_DIRECTORIES, SUPPORTED_EXTENSIONS
from pyreview.core.schemas import FileToReview


def load_files(
    paths: list[Path],
    settings: Settings,
) -> list[FileToReview]:
    """
    Accept a list of file paths or directories.
    For directories, recursively find all .py files.
    Respect max_file_size_kb and max_files limits.
    """
    collected: list[FileToReview] = []

    for path in paths:
        if path.is_file() and path.suffix in SUPPORTED_EXTENSIONS:
            _try_add(path, collected, settings)
        elif path.is_dir():
            for py_file in sorted(path.rglob("*.py")):
                if len(collected) >= settings.max_files:
                    break
                parts = py_file.parts
                if any(skip in parts for skip in SKIP_DIRECTORIES):
                    continue
                _try_add(py_file, collected, settings)

    return collected


def _try_add(path: Path, collected: list, settings: Settings) -> None:
    if len(collected) >= settings.max_files:
        return
    size_kb = path.stat().st_size / 1024
    if size_kb > settings.max_file_size_kb:
        return
    content = path.read_text(encoding="utf-8", errors="replace")
    collected.append(FileToReview(
        path=str(path),
        content=content,
        language="python",
    ))
