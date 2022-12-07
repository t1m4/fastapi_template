from app.types import StrDict


class BaseError(Exception):
    MESSAGE: str = "Base error"
    HTTP_STATUS: int = 400

    def __init__(
        self,
        message: str | None = None,
        status_code: int | None = None,
        extra: StrDict | None = None,
    ) -> None:
        self.message = message or self.MESSAGE
        self.http_status = status_code or self.HTTP_STATUS
        self.extra = extra
        super().__init__(self.message)


class DoesNotExistsError(BaseError):
    MESSAGE = "Object does not exist"
    HTTP_STATUS = 404
