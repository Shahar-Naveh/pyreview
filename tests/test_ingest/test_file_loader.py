"""Tests for the file loader."""

import pytest
from pathlib import Path

from pyreview.core.config import Settings
from pyreview.ingest.file_loader import load_files


def test_load_single_file(tmp_path):
    """Test loading a single Python file."""
    py_file = tmp_path / "test.py"
    py_file.write_text("print('hello')")

    settings = Settings(anthropic_api_key="test")
    files = load_files([py_file], settings)

    assert len(files) == 1
    assert files[0].content == "print('hello')"
    assert files[0].language == "python"


def test_load_directory(tmp_path):
    """Test loading all Python files from a directory."""
    (tmp_path / "a.py").write_text("x = 1")
    (tmp_path / "b.py").write_text("y = 2")
    (tmp_path / "c.txt").write_text("not python")

    settings = Settings(anthropic_api_key="test")
    files = load_files([tmp_path], settings)

    assert len(files) == 2
    paths = {f.path for f in files}
    assert any("a.py" in p for p in paths)
    assert any("b.py" in p for p in paths)


def test_respects_max_files(tmp_path):
    """Test that max_files limit is respected."""
    for i in range(10):
        (tmp_path / f"file_{i}.py").write_text(f"x = {i}")

    settings = Settings(anthropic_api_key="test", max_files=3)
    files = load_files([tmp_path], settings)

    assert len(files) == 3


def test_skips_large_files(tmp_path):
    """Test that files exceeding max_file_size_kb are skipped."""
    small = tmp_path / "small.py"
    small.write_text("x = 1")

    large = tmp_path / "large.py"
    large.write_text("x = 1\n" * 100_000)  # Very large file

    settings = Settings(anthropic_api_key="test", max_file_size_kb=1)
    files = load_files([tmp_path], settings)

    assert len(files) == 1
    assert "small.py" in files[0].path


def test_skips_venv_directories(tmp_path):
    """Test that .venv and __pycache__ are skipped."""
    (tmp_path / "good.py").write_text("x = 1")
    venv_dir = tmp_path / ".venv" / "lib"
    venv_dir.mkdir(parents=True)
    (venv_dir / "bad.py").write_text("y = 2")

    settings = Settings(anthropic_api_key="test")
    files = load_files([tmp_path], settings)

    assert len(files) == 1
    assert "good.py" in files[0].path
