from dataclasses import dataclass, field
from threading import Lock

from ai_support_desk.llm import Message


@dataclass(frozen=True, slots=True)
class ChatReply:
    text: str
    model: str
    session_id: str
    prompt_id: str
    prompt_version: str
    elapsed_seconds: float
    prompt_tokens: int | None
    completion_tokens: int | None
    total_tokens: int | None
    response_id: str
    history_messages: int
    context_history_messages: int
    removed_history_messages: int
    estimated_prompt_tokens: int
    summary_updated: bool = False
    has_summary: bool = False


@dataclass(slots=True)
class ChatSession:
    messages: list[Message] = field(default_factory=list)
    summary: str | None = None
    lock: Lock = field(default_factory=Lock)


@dataclass(frozen=True, slots=True)
class ChatTextDelta:
    text: str


@dataclass(frozen=True, slots=True)
class ChatStreamCompleted:
    result: ChatReply


type ChatStreamEvent = ChatTextDelta | ChatStreamCompleted
