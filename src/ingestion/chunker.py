"""Character-based text chunking for the ingestion pipeline.

Splits per-page text into fixed-size, overlapping chunks. Chunks never
span multiple pages, and text is preserved exactly as received — no
cleaning or normalization is performed here.
"""

from src.core.config import settings
from src.core.logging import logger


class TextChunker:
    """Splits per-page text into page-bounded, character-based chunks."""

    def __init__(self) -> None:
        """Read chunk sizing parameters from the shared application settings."""
        self.chunk_size: int = settings.chunk_size
        self.chunk_overlap: int = settings.chunk_overlap

    def chunk_pages(self, pages: list[str]) -> list[dict]:
        """Chunk a list of per-page text into character-based chunks.

        Args:
            pages: One string per page, in page order. Completely empty
                (or whitespace-only) pages are skipped.

        Returns:
            A list of chunk dictionaries, each containing `chunk_id`,
            `text`, `page_number`, `start_char`, and `end_char`. Page
            order and boundaries are preserved; no chunk crosses a
            page boundary.
        """
        chunks: list[dict] = []

        for page_index, page_text in enumerate(pages):
            page_number = page_index + 1

            if not page_text.strip():
                logger.info("Skipping empty page %d", page_number)
                continue

            chunks.extend(self._chunk_page(page_text, page_number))

        logger.info("Produced %d chunk(s) from %d page(s)", len(chunks), len(pages))
        return chunks

    def _chunk_page(self, text: str, page_number: int) -> list[dict]:
        """Chunk a single page's text using a sliding character window.

        Args:
            text: Raw text of the page, used exactly as provided.
            page_number: 1-indexed page number, used in chunk IDs.

        Returns:
            A list of chunk dictionaries for this page only.
        """
        page_chunks: list[dict] = []
        step = self.chunk_size - self.chunk_overlap
        text_length = len(text)

        start = 0
        local_index = 0

        while start < text_length:
            end = min(start + self.chunk_size, text_length)

            page_chunks.append(
                {
                    "chunk_id": f"p{page_number}_c{local_index}",
                    "text": text[start:end],
                    "page_number": page_number,
                    "start_char": start,
                    "end_char": end,
                }
            )

            local_index += 1
            if end == text_length:
                break
            start += step

        return page_chunks
