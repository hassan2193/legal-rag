"""Embedding generation for the retrieval pipeline.

Wraps a Sentence-Transformers model, loaded once at initialization, and
exposes single and batch embedding methods.
"""

from sentence_transformers import SentenceTransformer

from src.core.config import settings
from src.core.exceptions import RetrievalError
from src.core.logging import logger


class EmbeddingService:
    """Generates text embeddings using a Sentence-Transformers model."""

    def __init__(self) -> None:
        """Load the embedding model named in `settings.embedding_model`.

        The model is loaded exactly once and reused for all subsequent
        calls to `embed` and `embed_batch`.

        Raises:
            RetrievalError: If the embedding model fails to load.
        """
        logger.info("Loading embedding model: %s", settings.embedding_model)
        try:
            self._model: SentenceTransformer = SentenceTransformer(settings.embedding_model)
        except Exception as exc:
            logger.error("Failed to load embedding model %s: %s", settings.embedding_model, exc)
            raise RetrievalError(f"Failed to load embedding model: {settings.embedding_model}") from exc
        logger.info("Embedding model loaded: %s", settings.embedding_model)

    def embed(self, text: str) -> list[float]:
        """Generate an embedding vector for a single string.

        Args:
            text: Text to embed.

        Returns:
            The embedding vector as a list of floats.

        Raises:
            RetrievalError: If embedding generation fails.
        """
        logger.info("Generating embedding for 1 text (length=%d)", len(text))
        try:
            vector = self._model.encode(
    text,
    normalize_embeddings=True,
)
        except Exception as exc:
            logger.error("Embedding generation failed: %s", exc)
            raise RetrievalError("Failed to generate embedding for text.") from exc
        return vector.tolist()

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate embedding vectors for a batch of strings.

        Args:
            texts: List of texts to embed, in order.

        Returns:
            A list of embedding vectors, in the same order as `texts`.

        Raises:
            RetrievalError: If embedding generation fails.
        """
        logger.info("Generating embeddings for %d text(s)", len(texts))
        try:
            vectors = self._model.encode(
    texts,
    normalize_embeddings=True,
)
        except Exception as exc:
            logger.error("Batch embedding generation failed: %s", exc)
            raise RetrievalError("Failed to generate embeddings for text batch.") from exc
        return [vector.tolist() for vector in vectors]
