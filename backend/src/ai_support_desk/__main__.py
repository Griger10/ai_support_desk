from dotenv import load_dotenv
from pydantic import ValidationError

from ai_support_desk.chat import ChatService
from ai_support_desk.console import run_console
from ai_support_desk.conversation import ConversationSummaryService
from ai_support_desk.history import SlidingWindowHistory
from ai_support_desk.history.service import TokenCounter
from ai_support_desk.llm import LLMClient
from ai_support_desk.shared import Settings


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
    token_counter = TokenCounter()
    sliding_history = SlidingWindowHistory(
        token_counter=token_counter,
        input_token_budget=settings.chat_input_token_budget,
    )
    summary_service = ConversationSummaryService(llm_client)
    chat_service = ChatService(llm_client, sliding_history, summary_service)

    try:
        run_console(
            chat_service,
            app_env=settings.app_env,
            configured_model=settings.model,
        )
    finally:
        llm_client.close()


if __name__ == "__main__":
    main()
