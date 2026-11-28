from dataclasses import dataclass

from ai_support_desk.chat import ChatService
from ai_support_desk.conversation import ConversationSummaryService
from ai_support_desk.history.service import TokenCounter, SlidingWindowHistory
from ai_support_desk.llm import LLMClient
from ai_support_desk.shared import Settings
from ai_support_desk.support_request_analyzer import SupportRequestAnalyzer
from ai_support_desk.tools import BoundedToolLoop
from ai_support_desk.tools.default_registry import build_default_tool_registry
from ai_support_desk.tools.execution import ToolExecutor


@dataclass(slots=True, frozen=True)
class ApplicationContainer:
    settings: Settings
    chat_service: ChatService
    request_analyzer: SupportRequestAnalyzer
    llm_client: LLMClient
    tool_executor: ToolExecutor

    def close(self) -> None:
        try:
            self.tool_executor.close()
        finally:
            self.llm_client.close()


def build_application(settings: Settings) -> ApplicationContainer:
    llm_client = LLMClient(settings)

    tool_registry = build_default_tool_registry()
    tool_executor = ToolExecutor(tool_registry)
    tool_loop = BoundedToolLoop(
        client=llm_client,
        registry=tool_registry,
        executor=tool_executor,
        max_steps=settings.tool_max_steps,
    )

    token_counter = TokenCounter()
    history_policy = SlidingWindowHistory(
        token_counter=token_counter,
        input_token_budget=settings.chat_input_token_budget,
    )
    summary_service = ConversationSummaryService(llm_client)

    chat_service = ChatService(
        tool_loop=tool_loop,
        history_policy=history_policy,
        summary_service=summary_service,
    )
    request_analyzer = SupportRequestAnalyzer(llm_client)

    return ApplicationContainer(
        settings=settings,
        chat_service=chat_service,
        request_analyzer=request_analyzer,
        llm_client=llm_client,
        tool_executor=tool_executor,
    )
