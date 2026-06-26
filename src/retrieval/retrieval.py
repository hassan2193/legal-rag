"""Retriever module for fetching relevant chunks from the vector store."""

from src.core.exceptions import RetrievalError
from src.core.logging import logger
from src.embeddings.embeddings import EmbeddingService
from src.retrieval.vector_store import VectorStore


class Retriever:
    """Retrieves relevant document chunks using embeddings and FAISS."""

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
    ) -> None:
        """Initialize the retriever."""

        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def retrieve(self, query: str, k: int = 5) -> list[dict]:
        """Retrieve the top-k most relevant chunks for a query.

        Args:
            query: User query.
            k: Number of chunks to retrieve.

        Returns:
            List of retrieved chunk metadata.

        Raises:
            RetrievalError: If embedding generation or retrieval fails.
        """

        logger.info("Starting retrieval (k=%d)", k)

        try:
            query_embedding = self.embedding_service.embed(query)
        except Exception as exc:
            logger.error("Failed to generate query embedding: %s", exc)
            raise RetrievalError("Embedding generation failed.") from exc

        try:
            results = self.vector_store.search(query_embedding, k=k)
        except Exception as exc:
            logger.error("Failed to search vector store: %s", exc)
            raise RetrievalError("Vector store search failed.") from exc

        logger.info("Retrieval completed. Retrieved %d chunk(s).", len(results))

        return results