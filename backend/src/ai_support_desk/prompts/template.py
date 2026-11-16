from dataclasses import dataclass
from string import Template

from ai_support_desk.prompts.errors import PromptTemplateError


@dataclass(frozen=True, slots=True)
class PromptTemplate:
    prompt_id: str
    version: str
    body: str
    required_variables: frozenset[str]
    optional_variables: frozenset[str] = frozenset()

    def __post_init__(self) -> None:
        if not self.prompt_id.strip():
            raise PromptTemplateError("Идентификатор промпта не должен быть пустым.")
        if not self.version.strip():
            raise PromptTemplateError("Версия промпта не должна быть пустой.")

        duplicated = self.required_variables & self.optional_variables
        if duplicated:
            names = ", ".join(sorted(duplicated))
            raise PromptTemplateError(
                f"Переменные одновременно обязательные и необязательные: {names}."
            )

        template = Template(self.body)
        if not template.is_valid():
            raise PromptTemplateError("Текст содержит некорректную переменную шаблона.")

        placeholders = frozenset(template.get_identifiers())
        declared = self.required_variables | self.optional_variables
        if placeholders != declared:
            expected = ", ".join(sorted(declared)) or "нет"
            actual = ", ".join(sorted(placeholders)) or "нет"
            raise PromptTemplateError(
                "Переменные body не совпадают с объявленными. "
                f"Объявлены: {expected}. Найдены: {actual}."
            )

    def render(self, **variables: str | tuple[str, ...]) -> str:
        provided = frozenset(variables)
        missing = self.required_variables - provided
        if missing:
            names = ", ".join(sorted(missing))
            raise PromptTemplateError(f"Не переданы обязательные переменные: {names}.")

        allowed = self.required_variables | self.optional_variables
        unexpected = provided - allowed
        if unexpected:
            names = ", ".join(sorted(unexpected))
            raise PromptTemplateError(f"Переданы неизвестные переменные: {names}.")

        invalid = sorted(
            name
            for name, value in variables.items()
            if not isinstance(value, (str, tuple))
            or (isinstance(value, tuple) and not all(isinstance(item, str) for item in value))
        )
        if invalid:
            names = ", ".join(invalid)
            raise PromptTemplateError(
                f"Значения должны быть строками или кортежами строк: {names}."
            )

        normalized: dict[str, str] = {}
        for name, value in variables.items():
            normalized[name] = "\n".join(value) if isinstance(value, tuple) else value

        values = dict.fromkeys(self.optional_variables, "")
        values.update(normalized)

        return Template(self.body).substitute(values).strip()
