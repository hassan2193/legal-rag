"""Extraction agent orchestrating prompt building, generation, and validation."""

import json

from src.core.logging import logger
from src.core.exceptions import ExtractionError
from src.agents.prompts import PromptBuilder
from src.agents.gemini_client import GeminiClient
from src.agents.validation_agent import ValidationAgent


class ExtractionAgent:
    """Orchestrates the extraction workflow: prompt building, generation, and validation."""

    def __init__(
        self,
        prompt_builder: PromptBuilder,
        gemini_client: GeminiClient,
        validation_agent: ValidationAgent,
    ) -> None:
        """Initialize the ExtractionAgent with its collaborators.

        Args:
            prompt_builder: Builds the extraction prompt.
            gemini_client: Sends prompts to Gemini and returns raw text.
            validation_agent: Validates the parsed extraction result.
        """
        self.prompt_builder = prompt_builder
        self.gemini_client = gemini_client
        self.validation_agent = validation_agent

    def extract(self, query: str, chunks: list[dict], schema: dict) -> dict:
        """Run the full extraction workflow and return a validated result.

        Args:
            query: The user query describing what to extract.
            chunks: Retrieved chunk metadata to ground the extraction.
            schema: Target JSON schema the output must conform to.

        Returns:
            The validated extraction result.

        Raises:
            ExtractionError: If the Gemini response is not valid JSON.
        """
        logger.info("Extraction started")

        prompt = self.prompt_builder.build_prompt(query, chunks, schema)
        logger.info("Prompt built (length=%d chars)", len(prompt))

        raw_response = self.gemini_client.generate(prompt)
        if not raw_response.strip():
          raise ExtractionError("Gemini returned an empty response.")
        logger.info("Gemini response received (length=%d chars)", len(raw_response))

        try:
            parsed_result = json.loads(raw_response)
        except (json.JSONDecodeError, TypeError) as exc:
            logger.error("Failed to parse Gemini response as JSON: %s", exc)
            raise ExtractionError(f"Invalid JSON returned by Gemini.") from exc

        validated_result = self.validation_agent.validate(parsed_result, schema)
        logger.info("Validation completed")

        return validated_result