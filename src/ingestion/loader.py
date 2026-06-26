"""PDF text loading for the ingestion pipeline.

Extracts raw, per-page text from a PDF using pdfplumber. No cleaning,
normalization, or chunking is performed here — this module's only job
is to get text out of the file.
"""

from pathlib import Path

import pdfplumber

from src.core.exceptions import IngestionError
from src.core.logging import logger


class PDFLoader:
    """Loads raw, per-page text from a PDF file using pdfplumber."""

    def __init__(self, file_path: str | Path) -> None:
        """Store the path to the PDF that will be loaded.

        Args:
            file_path: Path to the PDF file to load.
        """
        self.file_path: Path = Path(file_path)

    def load_pages(self) -> list[str]:
        """Extract raw text from each page of the PDF, in page order.

        Returns:
            A list of strings, one per page, in the same order as the
            source document.

        Raises:
            IngestionError: If the file does not exist, the PDF cannot be
                opened, or no readable text is found in any page.
        """
        if not self.file_path.exists():
            logger.error("PDF file not found: %s", self.file_path)
            raise IngestionError(f"PDF file not found: {self.file_path}")
        logger.info("Opening PDF: %s", self.file_path)
        try:
            with pdfplumber.open(self.file_path) as pdf:
                pages: list[str] = [page.extract_text() or "" for page in pdf.pages]
        
        except Exception as exc:
            logger.error("Failed to open PDF %s: %s", self.file_path, exc)
            raise IngestionError(f"Failed to open PDF: {self.file_path}") from exc

        if not any(page.strip() for page in pages):
            logger.error("No readable text found in PDF: %s", self.file_path)
            raise IngestionError(f"No readable text found in PDF: {self.file_path}")

        logger.info("Loaded %d page(s) from PDF: %s", len(pages), self.file_path)
        return pages
