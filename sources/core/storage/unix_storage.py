import os
from sources.core.storage.storage import Storage


class UnixStorage(Storage):
    def __init__(self):
        super().__init__()
        self.base_folder = os.path.expanduser('~/.encrypt-me')
