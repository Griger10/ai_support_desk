from ai_support_desk.prompts.support_chat.registry import (
    get_support_chat_prompt,
    list_support_chat_versions,
    ACTIVE_SUPPORT_CHAT_VERSION,
)

SUPPORT_CHAT_PROMPT = get_support_chat_prompt()

__all__ = [
    "ACTIVE_SUPPORT_CHAT_VERSION",
    "SUPPORT_CHAT_PROMPT",
    "get_support_chat_prompt",
    "list_support_chat_versions",
]
