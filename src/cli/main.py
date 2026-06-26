"""CLI entry point for running the contract extraction pipeline."""

import json

import typer

from src.agents.extraction_agent import ExtractionAgent
from src.agents.gemini_client import GeminiClient
from src.agents.prompts import PromptBuilder
from src.agents.validation_agent import ValidationAgent
from src.core.exceptions import PipelineError
from src.core.logging import logger
from src.services.pipeline_service import PipelineService

app = typer.Typer()


@app.command()
def run(
    pdf: str = typer.Option(..., "--pdf", help="Path to the input PDF."),
    schema: str = typer.Option(..., "--schema", help="Path to the JSON schema."),
    query: str = typer.Option(..., "--query", help="Extraction query."),
    output: str = typer.Option(..., "--output", help="Output JSON file."),
) -> None:
    """Run the contract extraction pipeline."""

    logger.info("CLI started")

    try:
        with open(schema, "r", encoding="utf-8") as schema_file:
            schema_data = json.load(schema_file)
    except Exception as exc:
        logger.error("Failed to load schema: %s", exc)
        raise PipelineError("Failed to load schema.") from exc

    try:
        prompt_builder = PromptBuilder()
        gemini_client = GeminiClient()
        validation_agent = ValidationAgent()

        extraction_agent = ExtractionAgent(
            prompt_builder,
            gemini_client,
            validation_agent,
        )

        pipeline = PipelineService(extraction_agent)

    except Exception as exc:
        logger.error("Failed to initialize pipeline: %s", exc)
        raise PipelineError("Failed to initialize pipeline.") from exc

    try:
        result = pipeline.run(
            pdf_path=pdf,
            query=query,
            schema=schema_data,
        )

    except Exception as exc:
        logger.error("Pipeline execution failed: %s", exc)
        raise PipelineError("Pipeline execution failed.") from exc

    try:
        with open(output, "w", encoding="utf-8") as output_file:
            json.dump(
                result,
                output_file,
                indent=2,
                ensure_ascii=False,
            )

    except Exception as exc:
        logger.error("Failed to write output: %s", exc)
        raise PipelineError("Failed to write output file.") from exc

    logger.info("CLI completed successfully")


if __name__ == "__main__":
    app()