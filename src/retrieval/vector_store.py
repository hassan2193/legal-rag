"""FAISS-backed vector store for chunk embeddings and metadata.

Stores chunk embeddings in a FAISS `IndexFlatIP` index alongside their
original chunk metadata, and supports similarity search. Embeddings are
assumed to already be normalized, since `IndexFlatIP` computes plain
inner product (which is equivalent to cosine similarity on unit vectors).
"""

import faiss
import numpy as np

from src.core.exceptions import RetrievalError
from src.core.logging import logger


class VectorStore:
    """In-memory FAISS vector store pairing embeddings with chunk metadata."""

    def __init__(self) -> None:
        """Initialize an empty store. The FAISS index is created lazily on first `add`."""
        self._index: faiss.IndexFlatIP | None = None
        self._metadata: list[dict] = []

    def add(self, chunks: list[dict], embeddings: list[list[float]]) -> None:
        """Add chunk metadata and their corresponding embeddings to the store.

        Args:
            chunks: Chunk metadata dictionaries, in the same order as `embeddings`.
            embeddings: Pre-normalized embedding vectors, one per chunk.

        Raises:
            RetrievalError: If the number of chunks and embeddings don't match,
                or if adding to the FAISS index fails.
        """
        if len(chunks) != len(embeddings):
            logger.error(
                "Mismatched chunk/embedding counts: %d chunks, %d embeddings",
                len(chunks),
                len(embeddings),
            )
            raise RetrievalError("Number of chunks must match number of embeddings.")

        if not embeddings:
            logger.info("No chunks to add to vector store.")
            return

        try:
            vectors = np.asarray(embeddings, dtype="float32")

            if self._index is None:
                dimension = vectors.shape[1]
                self._index = faiss.IndexFlatIP(dimension)
                logger.info("Initialized FAISS IndexFlatIP with dimension %d", dimension)

            self._index.add(vectors)
            self._metadata.extend(chunks)
        
        except Exception as exc:
            logger.error("Failed to add chunks to vector store: %s", exc)
            raise RetrievalError("Failed to add chunks to the vector store.") from exc

        logger.info("Added %d chunk(s) to vector store (total=%d)", len(chunks), len(self._metadata))

    def search(self, query_embedding: list[float], k: int = 5) -> list[dict]:
        """Search the store for the `k` most similar chunks to a query embedding.

        Args:
            query_embedding: Pre-normalized query embedding vector.
            k: Maximum number of results to return.

        Returns:
            Chunk metadata dictionaries for the retrieved chunks, ordered by
            descending similarity.

        Raises:
            RetrievalError: If the store is empty or the search fails.
        """
        if self._index is None or self._index.ntotal == 0:
            logger.error("Search attempted on empty vector store.")
            raise RetrievalError("Cannot search an empty vector store.")

        try:
            query_vector = np.asarray([query_embedding], dtype="float32")
            top_k = min(k, self._index.ntotal)
            _, indices = self._index.search(query_vector, top_k)
        except Exception as exc:
            logger.error("Vector search failed: %s", exc)
            raise RetrievalError("Failed to search the vector store.") from exc

        results = [self._metadata[idx] for idx in indices[0] if idx != -1]
        logger.info("Retrieved %d chunk(s) for query (k=%d)", len(results), k)
        return results
