from ai_support_desk.tools.order_status import ORDER_STATUS_TOOL
from ai_support_desk.tools.registry import ToolRegistry


def build_default_tool_registry() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register(ORDER_STATUS_TOOL)
    return registry
