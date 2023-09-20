from sources.core.configuration import Configuration
from sources.core.formatter import Formatter


class Options:
    email: str = None
    password: str = None
    signature: bool = False
    ignore_signature: bool = False
    configuration: Configuration

    def __init__(self):
        self.configuration = Configuration()
        self.configuration.load_configuration()

    def get_password_bytes(self):
        if self.password is None:
            return None
        return bytes(self.password, Formatter.DEFAULT_ENCODING)
