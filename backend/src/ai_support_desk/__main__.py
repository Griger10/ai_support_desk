from dotenv import load_dotenv
from pydantic import ValidationError

from ai_support_desk.chat import ChatService
from ai_support_desk.console import run_console
from ai_support_desk.conversation import ConversationSummaryService
from ai_support_desk.history import SlidingWindowHistory
from ai_support_desk.history.service import TokenCounter
from ai_support_desk.llm import LLMClient
from ai_support_desk.shared import Settings
from ai_support_desk.support_request_analyzer import SupportRequestAnalyzer
from ai_support_desk.tools import BoundedToolLoop
from ai_support_desk.tools.default_registry import build_default_tool_registry
from ai_support_desk.tools.execution import ToolExecutor


def main() -> None:
    load_dotenv()
    try:
        settings = Settings()
    except ValidationError as error:
        print("Ошибка конфигурации:")
        for issue in error.errors():
            field = ".".join(str(part) for part in issue["loc"])
            print(f"- {field}: {issue['msg']}")
        return
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
    sliding_history = SlidingWindowHistory(
        token_counter=token_counter,
        input_token_budget=settings.chat_input_token_budget,
    )
    summary_service = ConversationSummaryService(llm_client)
    chat_service = ChatService(
        tool_loop=tool_loop, history_policy=sliding_history, summary_service=summary_service
    )
    request_analyzer = SupportRequestAnalyzer(llm_client)

    try:
        run_console(
            chat_service=chat_service,
            app_env=settings.app_env,
            configured_model=settings.model,
            analyzer=request_analyzer,
        )
    finally:
        llm_client.close()
        tool_executor.close()


if __name__ == "__main__":
    main()
