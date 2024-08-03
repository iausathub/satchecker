class ValidationError(Exception):
    """Exception raised for validation errors."""

    def __init__(self, status_code: int, message: str):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)
