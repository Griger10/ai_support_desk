from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SupportSummary:
    text: str
    model: str
    prompt_id: str
    prompt_version: str
    elapsed_seconds: float
    prompt_tokens: int | None
    completion_tokens: int | None
    total_tokens: int | None
    response_id: str
