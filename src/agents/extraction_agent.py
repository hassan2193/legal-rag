"""Extraction agent orchestrating prompt building, generation, and validation."""

import json

from src.core.logging import logger
from src.core.exceptions import ExtractionError
from src.agents.prompts import PromptBuilder
from src.agents.gemini_client import GeminiClient
from src.agents.validation_agent import ValidationAgent


class ExtractionAgent:
    """Orchestrates the extraction workflow."""

    def __init__(
        self,
        prompt_builder: PromptBuilder,
        gemini_client: GeminiClient,
        validation_agent: ValidationAgent,
    ) -> None:
        self.prompt_builder = prompt_builder
        self.gemini_client = gemini_client
        self.validation_agent = validation_agent

    def extract(
        self,
        query: str,
        chunks: list[dict],
        schema: dict,
    ) -> dict:
        """Run the complete extraction pipeline."""

        logger.info("Extraction started")

        prompt = self.prompt_builder.build_prompt(query, chunks, schema)
        logger.info("Prompt built (length=%d chars)", len(prompt))

        raw_response = self.gemini_client.generate(prompt)

        if not raw_response.strip():
            raise ExtractionError("Gemini returned an empty response.")

        logger.info(
            "Gemini response received (length=%d chars)",
            len(raw_response),
        )
        
        print("\n" + "=" * 80)
        print("RAW GEMINI RESPONSE:")
        print(raw_response)
        print("=" * 80 + "\n")

        try:
            parsed_result = self._parse_json(raw_response)
        except Exception as exc:
            logger.error("Failed to parse Gemini response as JSON: %s", exc)
            raise ExtractionError("Invalid JSON returned by Gemini.") from exc

        validated_result = self.validation_agent.validate(
            parsed_result,
            schema,
        )

        logger.info("Validation completed")

        return validated_result

    def _parse_json(self, raw_response: str) -> dict:
        """Extract and parse JSON from a Gemini response."""

        cleaned = raw_response.strip()

        # Remove markdown code fences if present
        if cleaned.startswith("```json"):
            cleaned = cleaned[len("```json"):].strip()

        elif cleaned.startswith("```"):
            cleaned = cleaned[len("```"):].strip()

        if cleaned.endswith("```"):
            cleaned = cleaned[:-3].strip()

        # Extract JSON object only
        start = cleaned.find("{")
        end = cleaned.rfind("}")

        if start == -1 or end == -1:
            raise ExtractionError(
                "No JSON object found in Gemini response."
            )

        cleaned = cleaned[start:end + 1]

        return json.loads(cleaned)