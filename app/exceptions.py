class BaseCustomException(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class NotAuthenticatedException(BaseCustomException):
    pass


class ValidationError(BaseCustomException):
    pass
