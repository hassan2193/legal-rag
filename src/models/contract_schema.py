"""Pydantic models for contract extraction."""

from datetime import date
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class Currency(str, Enum):
    USD = "USD"
    INR = "INR"
    EUR = "EUR"
    GBP = "GBP"
    OTHER = "Other"


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Party(BaseModel):
    model_config = ConfigDict(extra="forbid")

    legal_name: str | None = None
    address: str | None = None
    signatory_name: str | None = None
    signatory_title: str | None = None


class Parties(BaseModel):
    model_config = ConfigDict(extra="forbid")

    provider: Party
    client: Party


class ReimbursementCap(BaseModel):
    model_config = ConfigDict(extra="forbid")

    amount: float | None = None
    currency: Currency | None = None
    period: str | None = None


class Fees(BaseModel):
    model_config = ConfigDict(extra="forbid")

    headline_fee: float | None = None
    total_payable: float
    currency: Currency
    reimbursement_cap: ReimbursementCap | None = None


class Milestone(BaseModel):
    model_config = ConfigDict(extra="forbid")

    milestone_id: str
    deliverable: str
    target_date: date | None = None
    fee_percent_released: float


class Termination(BaseModel):
    model_config = ConfigDict(extra="forbid")

    notice_days_general: int | None = None
    notice_days_managed_services: int | None = None


class ValidationNote(BaseModel):
    model_config = ConfigDict(extra="forbid")

    field: str
    issue: str
    severity: Severity


class ContractExtraction(BaseModel):
    model_config = ConfigDict(extra="forbid")

    contract_id: str
    parties: Parties

    effective_date: date | None = Field(default=None)
    term_months: int | None = Field(default=None)

    fees: Fees
    milestones: list[Milestone]
    termination: Termination

    validation_notes: list[ValidationNote] = Field(default_factory=list)