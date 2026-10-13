"""Central settings for the rag_assistant package.

Values come from environment variables (loaded from the project-root .env by
whoever calls into this package first), with sensible defaults for the
training kit. `settings` is a module-level singleton — everything imports
the same instance.
"""

import os
from dataclasses import dataclass, field
from pathlib import Path

# src/rag_assistant/config/settings.py -> project root is three levels up.
PROJECT_ROOT = Path(__file__).resolve().parents[3]


@dataclass
class Settings:
    openai_api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))

    llm_model: str = field(default_factory=lambda: os.getenv("LLM_MODEL", "gpt-4o"))
    llm_temperature: float = field(default_factory=lambda: float(os.getenv("LLM_TEMPERATURE", "0.3")))
    llm_max_tokens: int = field(default_factory=lambda: int(os.getenv("LLM_MAX_TOKENS", "600")))

    chunk_size: int = field(default_factory=lambda: int(os.getenv("CHUNK_SIZE", "1000")))
    chunk_overlap: int = field(default_factory=lambda: int(os.getenv("CHUNK_OVERLAP", "150")))
    retriever_k: int = field(default_factory=lambda: int(os.getenv("RETRIEVER_K", "6")))

    logs_dir: Path = field(default_factory=lambda: PROJECT_ROOT / "logs")
    guardrails_config: Path = field(
        default_factory=lambda: Path(__file__).resolve().parent / "guardrails.yaml"
    )


settings = Settings()
