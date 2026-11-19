from dataclasses import dataclass

from ai_support_desk.llm import Message


@dataclass(frozen=True, slots=True)
class PreparedHistory:
    messages: list[Message]
    estimated_tokens: int
    context_history_messages: int
    removed_history_messages: int
