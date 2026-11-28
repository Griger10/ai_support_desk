from dotenv import load_dotenv
from pydantic import ValidationError

from ai_support_desk.console import run_console
from ai_support_desk.di import build_application
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

    application = build_application(settings)

    try:
        run_console(
            chat_service=application.chat_service,
            analyzer=application.request_analyzer,
            app_env=application.settings.app_env,
            configured_model=application.settings.model,
        )
    finally:
        application.close()


if __name__ == "__main__":
    main()
