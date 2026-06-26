"""Pydantic v2 models for the Track 1 ContractExtraction JSON schema.

Models are defined bottom-up: leaf/reusable models first, composed upward
into the root `ContractExtraction` model. No business logic or cross-field
validation is implemented here — this module is purely the data contract.
"""

from datetime import date
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class Currency(str, Enum):
    """Supported currency codes for monetary fields."""

    USD = "USD"
    INR = "INR"
    EUR = "EUR"
    GBP = "GBP"
    OTHER = "Other"


class Severity(str, Enum):
    """Severity level of a validation finding."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Party(BaseModel):
    """A contracting party (provider or client)."""

    model_config = ConfigDict(extra="forbid")

    legal_name: str = Field(..., description="Full legal name of the party.")
    address: str | None = Field(default=None, description="Registered address of the party.")
    signatory_name: str = Field(..., description="Name of the individual signing on behalf of the party.")
    signatory_title: str = Field(..., description="Title of the signatory as shown in the document.")


class ReimbursementCap(BaseModel):
    """Optional cap on reimbursable expenses."""

    model_config = ConfigDict(extra="forbid")

    amount: float | None = Field(default=None, description="Maximum reimbursable amount.")
    currency: Currency | None = Field(
    default=None,
    description="Currency of the reimbursement cap.",
  )
    period: str | None = Field(default=None, description="Period over which the cap applies (e.g. 'monthly').")


class Fees(BaseModel):
    """Fee structure for the contract."""

    model_config = ConfigDict(extra="forbid")

    headline_fee: float | None = Field(default=None, description="The sticker fee mentioned in the contract.")
    total_payable: float = Field(
        ...,
        description=(
            "The actual total amount the client will pay during the Initial Term, "
            "inclusive of all surcharges and one-time fees but exclusive of taxes."
        ),
    )
    currency: Currency = Field(..., description="Currency in which fees are denominated.")
    reimbursement_cap: ReimbursementCap | None = Field(
        default=None, description="Reimbursement cap details, if specified."
    )


class Milestone(BaseModel):
    """A single deliverable milestone and its associated fee release."""

    model_config = ConfigDict(extra="forbid")

    milestone_id: str = Field(..., description="Identifier for the milestone.")
    deliverable: str = Field(..., description="Description of the deliverable for this milestone.")
    target_date: date | None = Field(
    ...,
    description="ISO 8601 target date if determinable. Null if unknown or not specified.",
    )
    
    fee_percent_released: float = Field(
        ..., description="Percentage of the total fee released upon this milestone."
    )


class Termination(BaseModel):
    """Termination notice terms."""

    model_config = ConfigDict(extra="forbid")

    notice_days_general: int = Field(
        ..., description="Notice period in days for general termination of the Agreement."
    )
    notice_days_managed_services: int | None = Field(
    ...,
    description="Managed services notice period. Null if not specified.",
    )
    


class ValidationNote(BaseModel):
    """A single inconsistency, conflict, or ambiguity flagged by the Validator Agent."""

    model_config = ConfigDict(extra="forbid")

    field: str = Field(..., description="JSON path to the affected field (e.g. 'parties.client.signatory_title').")
    issue: str = Field(..., description="A short, factual description of the problem.")
    severity: Severity = Field(..., description="Severity of the flagged issue.")


class Parties(BaseModel):
    """The two contracting parties."""

    model_config = ConfigDict(extra="forbid")

    provider: Party = Field(..., description="The provider party to the contract.")
    client: Party = Field(..., description="The client party to the contract.")


class ContractExtraction(BaseModel):
    """Root schema for a single extracted contract."""

    model_config = ConfigDict(extra="forbid")

    contract_id: str = Field(
    ...,
    description="Unique contract identifier.",
    )
    parties: Parties = Field(..., description="The provider and client parties to the contract.")
    effective_date: date = Field(..., description="Effective date in ISO 8601 (YYYY-MM-DD).")
    term_months: int = Field(..., description="Initial term length in months.")
    fees: Fees = Field(..., description="Fee structure for the contract.")
    milestones: list[Milestone] = Field(..., description="Deliverable milestones and their fee releases.")
    termination: Termination = Field(..., description="Termination notice terms.")
    validation_notes: list[ValidationNote] = Field(
        ...,
        description=(
            "Inconsistencies, conflicts, or ambiguities detected by the Validator Agent. "
            "An empty list means none were found."
        ),
    )
