from ai_support_desk.tools.order_status import ORDER_STATUS_TOOL
from ai_support_desk.tools.registry import ToolRegistry
from ai_support_desk.tools.return_policy import RETURN_POLICY_TOOL
from ai_support_desk.tools.return_request import RETURN_REQUEST_TOOL


def build_default_tool_registry() -> ToolRegistry:
    registry = ToolRegistry()
    for tool in (
        ORDER_STATUS_TOOL,
        RETURN_POLICY_TOOL,
        RETURN_REQUEST_TOOL,
    ):
        registry.register(tool)
    return registry
