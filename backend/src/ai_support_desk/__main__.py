from pydantic import ValidationError

from ai_support_desk.console import run_console
from ai_support_desk.llm import LLMClient
from ai_support_desk.shared import Settings
from ai_support_desk.support import SupportService


def main() -> None:
    try:
        settings = Settings()
    except ValidationError as error:
        print("Ошибка конфигурации:")
        for issue in error.errors():
            field = ".".join(str(part) for part in issue["loc"])
            print(f"- {field}: {issue['msg']}")
        return

    llm_client = LLMClient(settings)
    support_service = SupportService(llm_client)

    run_console(
        support_service,
        app_env=settings.app_env,
        configured_model=settings.model,
    )


if __name__ == "__main__":
    main()
