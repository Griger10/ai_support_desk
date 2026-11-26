from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class OrderStatusAnswer:
    text: str
    tool_used: bool
    order_id: str | None
    model: str
    prompt_id: str
    prompt_version: str
    total_tokens: int | None
    response_ids: tuple[str, ...]
