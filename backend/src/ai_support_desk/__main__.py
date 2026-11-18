from dotenv import load_dotenv
from pydantic import ValidationError

from ai_support_desk.chat import ChatService
from ai_support_desk.console import run_console
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
    chat_service = ChatService(llm_client)

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
