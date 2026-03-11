"""Parse unified diffs into structured data for targeted review."""

from __future__ import annotations

from dataclasses import dataclass

from unidiff import PatchSet


@dataclass
class ChangedHunk:
    file_path: str
    source_start: int
    source_length: int
    target_start: int
    target_length: int
    added_lines: list[tuple[int, str]]
    removed_lines: list[tuple[int, str]]


def parse_diff(diff_text: str) -> list[ChangedHunk]:
    """Parse a unified diff string into structured ChangedHunk objects."""
    patch = PatchSet(diff_text)
    hunks = []
    for patched_file in patch:
        for hunk in patched_file:
            added = [
                (line.target_line_no, line.value)
                for line in hunk
                if line.is_added
            ]
            removed = [
                (line.source_line_no, line.value)
                for line in hunk
                if line.is_removed
            ]
            hunks.append(ChangedHunk(
                file_path=patched_file.path,
                source_start=hunk.source_start,
                source_length=hunk.source_length,
                target_start=hunk.target_start,
                target_length=hunk.target_length,
                added_lines=added,
                removed_lines=removed,
            ))
    return hunks
