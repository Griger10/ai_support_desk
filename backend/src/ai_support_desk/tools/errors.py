from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ai_support_desk.tools.dto import ToolAuditRecord, ToolConfirmationRequest


class ToolRegistryError(RuntimeError):
    pass


class DuplicateToolError(ToolRegistryError):
    pass


class ToolNotRegisteredError(ToolRegistryError):
    pass


class ToolBusinessError(RuntimeError):
    def __init__(self, message: str, code: str = "business_error") -> None:
        super().__init__(message)
        self.code = code


class ToolExecutionError(RuntimeError):
    def __init__(self, message: str, audit: ToolAuditRecord) -> None:
        super().__init__(message)
        self.audit = audit


class ToolNotAllowedError(ToolExecutionError):
    pass


class ToolArgumentsError(ToolExecutionError):
    pass


class ToolTimeoutError(ToolExecutionError):
    pass


class ToolTechnicalError(ToolExecutionError):
    pass


class ToolLoopError(RuntimeError):
    pass


class ToolLoopProtocolError(ToolLoopError):
    pass


class ToolLoopLimitError(ToolLoopError):
    pass


class ToolLoopExecutionError(ToolLoopError):
    def __init__(self, message: str, audit: ToolAuditRecord) -> None:
        super().__init__(message)
        self.audit = audit


class ToolConfirmationRequiredError(ToolExecutionError):
    def __init__(
        self,
        message: str,
        audit: ToolAuditRecord,
        request: ToolConfirmationRequest,
    ) -> None:
        super().__init__(message, audit)
        self.request = request


class ToolConfirmationNotFoundError(RuntimeError):
    pass
