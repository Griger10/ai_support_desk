from dataclasses import dataclass
from enum import StrEnum
from typing import Final

from ai_support_desk.models import SupportRequestAnalysis

MIN_AUTOMATIC_CONFIDENCE: Final[float] = 0.75


@dataclass(frozen=True, slots=True)
class SupportRequestResult:
    analysis: SupportRequestAnalysis
    model: str
    prompt_id: str
    prompt_version: str
    elapsed_seconds: float
    prompt_tokens: int | None
    completion_tokens: int | None
    total_tokens: int | None
    response_id: str
    repair_attempts: int


class ReviewReason(StrEnum):
    LOW_CONFIDENCE = "low_confidence"
    HIGH_URGENCY = "high_urgency"
    UNKNOWN_CATEGORY = "unknown_category"
    REPAIRED_RESULT = "repaired_result"


@dataclass(frozen=True, slots=True)
class SupportRequestDecision:
    result: SupportRequestResult
    requires_human_review: bool
    review_reasons: tuple[ReviewReason, ...]
