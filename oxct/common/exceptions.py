class OxctError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class OxctNotFoundError(OxctError):
    pass
