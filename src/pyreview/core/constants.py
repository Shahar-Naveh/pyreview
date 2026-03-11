"""Constants used across the pyreview system."""

SUPPORTED_LANGUAGES = {"python", "py"}
SUPPORTED_EXTENSIONS = {".py"}
SKIP_DIRECTORIES = {"__pycache__", ".venv", "venv", "node_modules", ".git", ".eggs", "dist", "build"}

DEFAULT_MAX_FILE_SIZE_KB = 500
DEFAULT_MAX_FILES = 20

AGENT_NAMES = ("security", "performance", "style", "architecture", "engineering")
