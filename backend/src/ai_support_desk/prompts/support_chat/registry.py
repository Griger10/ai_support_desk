from ai_support_desk.prompts.errors import PromptTemplateError
from ai_support_desk.prompts.support_chat.v1_0_0 import SUPPORT_CHAT_PROMPT_V1_0_0
from ai_support_desk.prompts.support_chat.v1_1_0 import SUPPORT_CHAT_PROMPT_V1_1_0
from ai_support_desk.prompts.support_chat.v1_2_0 import SUPPORT_CHAT_PROMPT_V1_2_0
from ai_support_desk.prompts.support_chat.v1_3_0 import SUPPORT_CHAT_PROMPT_V1_3_0
from ai_support_desk.prompts.template import PromptTemplate

ACTIVE_SUPPORT_CHAT_VERSION = "1.3.0"


_SUPPORT_CHAT_PROMPTS: dict[str, PromptTemplate] = {
    SUPPORT_CHAT_PROMPT_V1_0_0.version: SUPPORT_CHAT_PROMPT_V1_0_0,
    SUPPORT_CHAT_PROMPT_V1_1_0.version: SUPPORT_CHAT_PROMPT_V1_1_0,
    SUPPORT_CHAT_PROMPT_V1_2_0.version: SUPPORT_CHAT_PROMPT_V1_2_0,
    SUPPORT_CHAT_PROMPT_V1_3_0.version: SUPPORT_CHAT_PROMPT_V1_3_0,
}


def get_support_chat_prompt(
    version: str | None = None,
) -> PromptTemplate:
    selected_version = ACTIVE_SUPPORT_CHAT_VERSION if version is None else version.strip()

    try:
        return _SUPPORT_CHAT_PROMPTS[selected_version]
    except KeyError as error:
        available = ", ".join(_SUPPORT_CHAT_PROMPTS)
        raise PromptTemplateError(
            f"Неизвестная версия support_chat: {selected_version}. Доступны: {available}."
        ) from error


def list_support_chat_versions() -> tuple[str, ...]:
    return tuple(_SUPPORT_CHAT_PROMPTS)
