from ai_support_desk.tools.order_status import ORDER_STATUS_TOOL
from ai_support_desk.tools.registry import ToolRegistry
from ai_support_desk.tools.return_policy import RETURN_POLICY_TOOL


def build_default_tool_registry() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register(ORDER_STATUS_TOOL)
    registry.register(RETURN_POLICY_TOOL)
    return registry
