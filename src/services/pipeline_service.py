"""Pipeline service orchestrating the end-to-end extraction workflow."""

from src.agents.extraction_agent import ExtractionAgent
from src.core.exceptions import PipelineError
from src.core.logging import logger
from src.embeddings.embeddings import EmbeddingService
from src.ingestion.chunker import TextChunker
from src.ingestion.loader import PDFLoader
from src.retrieval.retrieval import Retriever
from src.retrieval.vector_store import VectorStore


class PipelineService:
    """Coordinates the complete contract extraction pipeline."""

    def __init__(self, extraction_agent: ExtractionAgent) -> None:
        """Initialize all pipeline components."""

        self.extraction_agent = extraction_agent
        self.chunker = TextChunker()
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()
        self.retriever = Retriever(
            self.embedding_service,
            self.vector_store,
        )

    def run(
        self,
        pdf_path: str,
        query: str,
        schema: dict,
    ) -> dict:
        """Run the complete extraction pipeline."""

        logger.info("Pipeline started")

        try:
            loader = PDFLoader(pdf_path)
            pages = loader.load_pages()

            chunks = self.chunker.chunk_pages(pages)

            texts = [chunk["text"] for chunk in chunks]
            embeddings = self.embedding_service.embed_batch(texts)

            self.vector_store.add(chunks, embeddings)

            retrieved_chunks = self.retriever.retrieve(query)

            result = self.extraction_agent.extract(
                query=query,
                chunks=retrieved_chunks,
                schema=schema,
            )

            logger.info("Pipeline completed successfully")
            return result

        except Exception as exc:
            logger.error("Pipeline failed: %s", exc)
            raise PipelineError("Pipeline execution failed.") from exc