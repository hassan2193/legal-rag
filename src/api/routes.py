"""API routes for the contract extraction pipeline."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from src.agents.extraction_agent import ExtractionAgent
from src.agents.gemini_client import GeminiClient
from src.agents.prompts import PromptBuilder
from src.agents.validation_agent import ValidationAgent
from src.core.exceptions import PipelineError
from src.core.logging import logger
from src.services.pipeline_service import PipelineService

router = APIRouter()


class ExtractRequest(BaseModel):
    """Request model for the extraction endpoint."""

    pdf_path: str
    query: str
    schema: dict


@router.post("/extract")
def extract(request: ExtractRequest) -> dict:
    """Execute the contract extraction pipeline."""

    logger.info("Extraction request received")

    try:
        extraction_agent = ExtractionAgent(
            PromptBuilder(),
            GeminiClient(),
            ValidationAgent(),
        )

        pipeline = PipelineService(extraction_agent)

        result = pipeline.run(
            pdf_path=request.pdf_path,
            query=request.query,
            schema=request.schema,
        )

        logger.info("Extraction completed successfully")

        return result

    except PipelineError as exc:
        logger.error("Pipeline failed: %s", exc)
        raise HTTPException(
            status_code=500,
            detail="Pipeline execution failed.",
        ) from exc

    except Exception as exc:
        logger.exception("Unexpected server error")
        raise HTTPException(
            status_code=500,
            detail="Internal server error.",
        ) from exc