"""Application configuration loaded from environment variables and a `.env` file.

This module defines the single, type-safe source of truth for runtime
configuration used across the contract extraction pipeline.
"""

from typing import Literal

from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centralized application settings.

    Values are resolved from environment variables first, falling back to a
    `.env` file in the project root. Field types are validated by Pydantic
    on instantiation, so invalid or missing configuration fails fast at
    startup rather than surfacing later as a runtime error.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    google_api_key: SecretStr = Field(
        ...,
        description="API key used to authenticate requests to the Google Generative AI API.",
    )

    embedding_model: str = Field(
        default="BAAI/bge-small-en-v1.5",
        description="Name or path of the Sentence-Transformers embedding model to load.",
    )

    vector_store: Literal["faiss"] = Field(
        default="faiss",
        description="Backend used for vector similarity search.",
    )

    chunk_size: int = Field(
        default=1000,
        gt=0,
        description="Maximum number of characters per document chunk.",
    )

    chunk_overlap: int = Field(
        default=200,
        ge=0,
        description="Number of overlapping characters between consecutive chunks.",
    )

    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO",
        description="Minimum severity level emitted by the application logger.",
    )

    @model_validator(mode="after")
    def validate_chunk_overlap(self) -> "Settings":
        """Ensure `chunk_overlap` is strictly smaller than `chunk_size`."""
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError(
                f"chunk_overlap ({self.chunk_overlap}) must be smaller than "
                f"chunk_size ({self.chunk_size})."
            )
        return self


settings: Settings = Settings()
"""Singleton `Settings` instance shared across the application."""
