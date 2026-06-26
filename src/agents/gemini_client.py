"""Gemini client wrapper for the extraction agent."""

from langchain_google_genai import ChatGoogleGenerativeAI

from src.core.logging import logger
from src.core.exceptions import ExtractionError
from src.core.config import settings


class GeminiClient:
    """Wraps ChatGoogleGenerativeAI to provide deterministic text generation."""

    def __init__(self, model: str = "gemini-2.5-flash") -> None:
        """Initialize the Gemini client with a single model instance.

        Args:
            model: The Gemini model name to use.
        """
        try:
            self._model = ChatGoogleGenerativeAI(
                model=model,
                google_api_key=settings.google_api_key.get_secret_value(),
                temperature=0,
            )
        except Exception as exc:
            logger.error("Failed to initialize Gemini model: %s", exc)
            raise ExtractionError(f"Gemini model initialization failed: {exc}") from exc

    def generate(self, prompt: str) -> str:
        """Generate a raw text response from Gemini for the given prompt.

        Args:
            prompt: The fully constructed prompt string.

        Returns:
            The raw text content of the model's response.

        Raises:
            ExtractionError: If generation fails.
        """
        logger.info("Sending prompt to Gemini (length=%d chars)", len(prompt))

        try:
            response = self._model.invoke(prompt)
        except Exception as exc:
            logger.error("Gemini generation failed: %s", exc)
            raise ExtractionError(f"Gemini generation failed: {exc}") from exc

        logger.info("Received response from Gemini")

        return str(response.content)