from typing import Optional


class ValidationError(Exception):
    """Exception raised for validation errors."""

    def __init__(
        self,
        status_code: int,
        message: str,
        original_exception: Optional[Exception] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.original_exception = original_exception
        super().__init__(self.message)


class DataError(Exception):
    """Exception raised for data related errors."""

    def __init__(
        self,
        status_code: int,
        message: str,
        original_exception: Optional[Exception] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.original_exception = original_exception
        super().__init__(self.message)
