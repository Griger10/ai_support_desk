from typing import Any

from ai_support_desk.tools import RegisteredTool, ToolNotRegisteredError, DuplicateToolError


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, RegisteredTool[Any, Any]] = {}

    def register(self, tool: RegisteredTool[Any, Any]) -> None:
        if tool.name in self._tools:
            raise DuplicateToolError(f"Инструмент уже зарегистрирован: {tool.name}.")

        self._tools[tool.name] = tool

    def get(self, name: str) -> RegisteredTool[Any, Any]:
        try:
            return self._tools[name]
        except KeyError as error:
            raise ToolNotRegisteredError(f"Инструмент не зарегистрирован: {name}.") from error

    def names(self) -> tuple[str, ...]:
        return tuple(self._tools)

    def api_schemas(self) -> list[dict[str, Any]]:
        return [tool.to_api_schema() for tool in self._tools.values()]
