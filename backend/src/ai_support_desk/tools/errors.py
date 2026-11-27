class ToolRegistryError(RuntimeError):
    pass


class DuplicateToolError(ToolRegistryError):
    pass


class ToolNotRegisteredError(ToolRegistryError):
    pass
