
class FSOException(Exception):
    def __init__(self, message):
        super(FSOException, self).__init__(message)


class FSOHashException(FSOException):
    def __init__(self, message):
        super(FSOHashException, self).__init__(message)


class FSOTypeException(FSOException):
    def __init__(self, message):
        super(FSOTypeException, self).__init__(message)


class FSOTimeException(FSOException):
    def __init__(self, message):
        super(FSOTimeException, self).__init__(message)


class FSOMetaTypeException(FSOException):
    def __init__(self, message):
        super(FSOMetaTypeException, self).__init__(message)
