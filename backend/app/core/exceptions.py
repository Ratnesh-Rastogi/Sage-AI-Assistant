"""
Custom application exceptions.

Hierarchy defined in SAGE_BLUEPRINT.md Section 102:

BaseApplicationException
├── DatabaseException
├── ToolExecutionException
├── ProviderException
├── ValidationException
└── MemoryException
"""


class BaseApplicationException(Exception):
    """Base class for all application-specific exceptions."""

    code: str = "APPLICATION_ERROR"

    def __init__(self, message: str, code: str | None = None):
        self.message = message
        if code:
            self.code = code
        super().__init__(message)

    def to_dict(self) -> dict:
        return {
            "success": False,
            "error": {
                "code": self.code,
                "message": self.message,
            },
        }


class DatabaseException(BaseApplicationException):
    code = "DATABASE_ERROR"


class ToolExecutionException(BaseApplicationException):
    code = "TOOL_EXECUTION_ERROR"


class ProviderException(BaseApplicationException):
    code = "PROVIDER_ERROR"


class ValidationException(BaseApplicationException):
    code = "VALIDATION_ERROR"


class MemoryException(BaseApplicationException):
    code = "MEMORY_ERROR"


class NotFoundException(BaseApplicationException):
    code = "NOT_FOUND"
