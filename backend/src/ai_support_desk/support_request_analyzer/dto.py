from dataclasses import dataclass

from ai_support_desk.models import SupportRequestAnalysis


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
