import logging
import os
from time import perf_counter

import openai
from dotenv import load_dotenv
from openai import OpenAI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://api.proxyapi.ru/v1"
MODEL = "deepseek/deepseek-v4.1-flash-1017"
TEMPERATURE = 0.2
MAX_OUTPUT_TOKENS = 250

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


def summarize_request(client: OpenAI, user_text: str) -> None:
    """Кратко пересказывает обращение и печатает метрики запроса."""
    text = user_text.strip()
    if not text:
        logger.info("Ошибка: обращение не должно быть пустым.")
        return

    started_at = perf_counter()

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=build_messages(user_text),  # type: ignore[arg-type]
            temperature=TEMPERATURE,
            max_completion_tokens=MAX_OUTPUT_TOKENS,
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
    choice = response.choices[0]
    answer = choice.message.content

    logger.info("\nРезультат:")
    logger.info(answer or "Модель не вернула текстовый ответ")

    logger.info("\nМетрики:")
    logger.info(f"Модель: {response.model}")
    logger.info(f"Завершение: {choice.finish_reason}")
    logger.info(f"Время: {elapsed_seconds:.2f} с")

    if response.usage is not None:
        logger.info(f"Входные токены: {response.usage.prompt_tokens}")
        logger.info(f"Выходные токены: {response.usage.completion_tokens}")
        logger.info(f"Всего токенов: {response.usage.total_tokens}")

    logger.info(f"ID ответа: {response.id}")


def main() -> None:
    load_dotenv()

    token = os.getenv("LLM_API_KEY")
    if not token:
        raise SystemExit("Не найдена переменная LLM_API_KEY. Проверьте файл .env в корне проекта.")

    client = OpenAI(base_url=BASE_URL, api_key=token)
    user_text = input("Введите текст обращения: ")
    summarize_request(client, user_text)


if __name__ == "__main__":
    main()
