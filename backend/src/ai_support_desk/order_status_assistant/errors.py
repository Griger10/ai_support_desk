class OrderStatusAssistantError(RuntimeError):
    pass


class UnknownToolError(OrderStatusAssistantError):
    pass


class InvalidToolArgumentsError(OrderStatusAssistantError):
    pass


class UnexpectedToolFlowError(OrderStatusAssistantError):
    pass
