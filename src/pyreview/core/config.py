"""Layered configuration: .env -> environment variables -> config.yaml -> CLI flags."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import yaml
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AgentConfig(BaseSettings):
    """Per-agent tunables."""
    enabled: bool = True
    model: str = "claude-sonnet-4-5-20250929"
    max_tokens: int = 4096
    temperature: float = 0.2


class Settings(BaseSettings):
    """Root configuration for pyreview."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="PYREVIEW_",
        env_nested_delimiter="__",
        case_sensitive=False,
    )

    # --- API Keys ---
    anthropic_api_key: SecretStr = SecretStr("")
    github_token: Optional[SecretStr] = None

    # --- Claude Defaults ---
    default_model: str = "claude-sonnet-4-5-20250929"
    orchestrator_model: str = "claude-sonnet-4-5-20250929"

    # --- Agent Config ---
    security: AgentConfig = Field(default_factory=AgentConfig)
    performance: AgentConfig = Field(default_factory=AgentConfig)
    style: AgentConfig = Field(default_factory=AgentConfig)
    architecture: AgentConfig = Field(default_factory=AgentConfig)
    engineering: AgentConfig = Field(default_factory=AgentConfig)

    # --- Behavior ---
    max_file_size_kb: int = 500
    max_files: int = 20
    parallel_agents: bool = True
    severity_threshold: str = "low"

    # --- Web ---
    web_host: str = "127.0.0.1"
    web_port: int = 8000

    # --- Storage ---
    db_path: str = "~/.pyreview/reviews.db"

    @classmethod
    def from_yaml(cls, path: Path, **overrides) -> Settings:
        """Load from YAML file, then overlay env vars and explicit overrides."""
        if path.exists():
            with open(path) as f:
                yaml_data = yaml.safe_load(f) or {}
        else:
            yaml_data = {}
        yaml_data.update(overrides)
        return cls(**yaml_data)
