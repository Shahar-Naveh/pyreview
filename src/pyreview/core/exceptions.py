"""Custom exception hierarchy for pyreview."""


class PyReviewError(Exception):
    """Base exception for all pyreview errors."""


class ConfigError(PyReviewError):
    """Configuration-related errors."""


class AgentError(PyReviewError):
    """Error during agent execution."""


class ParseError(PyReviewError):
    """Error parsing Claude's response."""


class IngestError(PyReviewError):
    """Error loading or parsing source files."""


class GitHubError(PyReviewError):
    """Error interacting with GitHub API."""


class StorageError(PyReviewError):
    """Error with the storage layer."""
