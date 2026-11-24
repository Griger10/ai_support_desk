from ai_support_desk.models import SupportRequestAnalysis

SUPPORT_REQUEST_SCHEMA_NAME = "support_request"
SUPPORT_REQUEST_SCHEMA = SupportRequestAnalysis.model_json_schema()
