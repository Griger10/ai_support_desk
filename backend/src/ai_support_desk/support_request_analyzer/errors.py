class SupportRequestAnalyzerError(RuntimeError):
    pass


class SupportRequestRefusalError(SupportRequestAnalyzerError):
    pass


class IncompleteSupportRequestError(SupportRequestAnalyzerError):
    pass


class InvalidSupportRequestError(SupportRequestAnalyzerError):
    pass
