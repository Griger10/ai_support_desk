from dataclasses import dataclass
from re import fullmatch
from typing import Any
from collections.abc import Callable

from pydantic import BaseModel


@dataclass(frozen=True, slots=True)
class RegisteredTool[ArgumentsT: BaseModel, ResultT: BaseModel]:
    name: str
    description: str
    arguments_model: type[ArgumentsT]
    handler: Callable[[ArgumentsT], ResultT]
    timeout_seconds: float = 2.0

    def __post_init__(self) -> None:
        if fullmatch(r"[a-z][a-z0-9_]{0,63}", self.name) is None:
            raise ValueError(
                "Имя инструмента должно начинаться "
                "с буквы и содержать только "
                "строчные буквы, цифры и _."
            )

        if not self.description.strip():
            raise ValueError("Описание инструмента не должно быть пустым.")

        if self.timeout_seconds <= 0:
            raise ValueError("Timeout инструмента должен быть больше нуля.")

    def to_api_schema(self) -> dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description.strip(),
                "strict": True,
                "parameters": self.arguments_model.model_json_schema(),
            },
        }
