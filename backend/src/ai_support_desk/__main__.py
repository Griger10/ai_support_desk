import logging
from time import perf_counter

import openai
from pydantic import ValidationError

from ai_support_desk.llm import LLMClient, LLMResult
from ai_support_desk.shared import Settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SYSTEM_INSTRUCTION = (
    "Ты помогаешь оператору службы поддержки. "
    "Кратко пересказывай обращение одним предложением. "
    "Используй только факты из обращения. "
    "Не придумывай суммы, даты, причины и действия. "
    "Если данных недостаточно, прямо сообщай об этом."
)


def build_messages(user_text: str) -> list[dict[str, str]]:
    return [
        {
            "role": "system",
            "content": SYSTEM_INSTRUCTION,
        },
        {
            "role": "user",
            "content": f"Обращение:\n{user_text}",
        },
    ]


def print_usage(result: LLMResult) -> None:
    if result.total_tokens is None:
        logger.info("Провайдер не вернул статистику токенов.")
        return

    logger.info(f"Входные токены: {result.prompt_tokens}")
    logger.info(f"Выходные токены: {result.completion_tokens}")
    logger.info(f"Всего токенов: {result.total_tokens}")


def summarize_request(client: LLMClient, user_text: str) -> None:
    """Кратко пересказывает обращение и печатает метрики запроса."""
    text = user_text.strip()
    if not text:
        logger.info("Ошибка: обращение не должно быть пустым.")
        return

    started_at = perf_counter()

    try:
        result = client.generate(
            messages=build_messages(user_text),
        )
    except openai.AuthenticationError:
        logger.info("Ошибка авторизации: проверьте LLM_API_KEY.")
        return
    except openai.PermissionDeniedError:
        logger.info("Нет доступа к модели: проверьте разрешения API-ключа.")
        return
    except openai.RateLimitError:
        logger.info("Достигнут лимит запросов провайдера. Повторите запрос позднее.")
        return
    except openai.APITimeoutError:
        logger.info("ProxyAPI не успел ответить за отведенное время.")
        return
    except openai.APIConnectionError:
        logger.info("Не удалось соединиться с ProxyAPI. Проверьте сеть.")
        return
    except openai.APIStatusError as error:
        if error.status_code == 402:
            logger.info("Недостаточно средств на балансе ProxyAPI.")
        else:
            logger.info(f"API вернул ошибку со статусом {error.status_code}.")
        if error.request_id:
            logger.info(f"Request ID: {error.request_id}")
        return

    elapsed_seconds = perf_counter() - started_at
    answer = result.text

    logger.info("\nРезультат:")
    logger.info(answer or "Модель не вернула текстовый ответ")

    logger.info("\nМетрики:")
    logger.info(f"Модель: {result.model}")
    logger.info(f"Завершение: {result.finish_reason}")
    logger.info(f"Время: {elapsed_seconds:.2f} с")

    print_usage(result)

    logger.info(f"ID ответа: {result.response_id}")


def main() -> None:
    try:
        settings = Settings()
    except ValidationError as error:
        logger.error("Ошибка конфигурации:")
        for issue in error.errors():
            field = ".".join(str(part) for part in issue["loc"])
            logger.error(f"- {field}: {issue['msg']}")
        return

    client = LLMClient(
        settings=settings,
    )
    user_text = input("Введите текст обращения: ")
    summarize_request(client, user_text)


if __name__ == "__main__":
    main()
