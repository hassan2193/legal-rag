"""Validation agent for verifying extracted contract data against the schema."""

from pydantic import ValidationError as PydanticValidationError

from src.core.exceptions import ValidationError
from src.core.logging import logger
from src.models.contract_schema import ContractExtraction


class ValidationAgent:
    """Validates extracted JSON against the ContractExtraction schema."""

    def validate(self, data: dict, schema: dict) -> dict:
        """Validate extracted data using the ContractExtraction model.

        Args:
            data: Parsed extraction result.
            schema: Reserved for future schema-based validation.

        Returns:
            A validated dictionary.

        Raises:
            ValidationError: If schema validation fails.
        """
        logger.info("Validation started")

        try:
            validated_model = ContractExtraction.model_validate(data)
            validated_data = validated_model.model_dump()

            logger.info("Validation succeeded")
            return validated_data

        except PydanticValidationError as exc:
            logger.error("Schema validation failed: %s", exc)

            validation_notes = list(data.get("validation_notes", []))

            for error in exc.errors():
                field = ".".join(str(loc) for loc in error.get("loc", []))
                validation_notes.append(
                    {
                        "field": field,
                        "issue": error.get("msg", "Validation error"),
                        "severity": "high",
                    }
                )

            data["validation_notes"] = validation_notes

            raise ValidationError("Schema validation failed.") from exc