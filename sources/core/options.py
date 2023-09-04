from sources.core.formatter import Formatter


class Options:
    email: str = None
    password: str = None

    def get_password_bytes(self):
        return bytes(self.password, Formatter.DEFAULT_ENCODING)
