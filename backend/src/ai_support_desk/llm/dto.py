from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LLMResult:
    text: str | None
    model: str
    finish_reason: str | None
    prompt_tokens: int | None
    completion_tokens: int | None
    total_tokens: int | None
    response_id: str
    refusal: str | None
    tool_calls: tuple[ToolCall, ...]


@dataclass(frozen=True, slots=True)
class LLMTextDelta:
    text: str


@dataclass(frozen=True, slots=True)
class LLMStreamCompleted:
    model: str
    finish_reason: str | None
    prompt_tokens: int | None
    completion_tokens: int | None
    total_tokens: int | None
    response_id: str


@dataclass(frozen=True, slots=True)
class ToolCall:
    id: str
    name: str
    arguments: str


type LLMStreamEvent = LLMTextDelta | LLMStreamCompleted
