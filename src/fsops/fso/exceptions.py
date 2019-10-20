
class FSOException(Exception):
    def __init__(self, message):
        super().__init__(message)


class FSOHashException(FSOException):
    def __init__(self, message):
        super().__init__(message)


class FSOTypeException(FSOException):
    def __init__(self, message):
        super().__init__(message)


class FSOTimeException(FSOException):
    def __init__(self, message):
        super().__init__(message)


class FSOMetaTypeException(FSOException):
    def __init__(self, message):
        super().__init__(message)
