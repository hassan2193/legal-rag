"""Custom exception hierarchy for the Legal RAG pipeline.

All project-specific exceptions inherit from `LegalRAGError`, allowing
callers to catch every domain error with a single `except LegalRAGError`
clause while still distinguishing failure types when needed.
"""


class LegalRAGError(Exception):
    """Base exception for all errors raised by the Legal RAG pipeline."""


class ConfigurationError(LegalRAGError):
    """Raised when required configuration is missing or invalid at startup."""


class IngestionError(LegalRAGError):
    """Raised when a document fails to load, parse, or be cleaned/chunked."""


class RetrievalError(LegalRAGError):
    """Raised when the vector store or retriever fails to return results."""


class ExtractionError(LegalRAGError):
    """Raised when the extraction agent fails to produce a valid schema-conformant result."""


class ValidationError(LegalRAGError):
    """Raised when the validation agent fails to complete its consistency checks."""

class PipelineError(LegalRAGError):
    """Raised when the end-to-end pipeline fails."""