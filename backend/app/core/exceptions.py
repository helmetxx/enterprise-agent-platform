from typing import Any, Optional

class AppException(Exception):
    def __init__(
        self,
        message: str,
        code: str = "error",
        status_code: int = 400,
        data: Optional[Any] = None
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.data = data
        super().__init__(message)

class AuthenticationError(AppException):
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(
            message=message,
            code="authentication_error",
            status_code=401
        )

class PermissionDenied(AppException):
    def __init__(self, message: str = "Permission denied"):
        super().__init__(
            message=message,
            code="permission_denied",
            status_code=403
        )

class NotFound(AppException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(
            message=message,
            code="not_found",
            status_code=404
        ) 