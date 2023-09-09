import os
from sources.core.storage.storage import Storage


class WindowsStorage(Storage):
    def __int__(self):
        super().__init__()
        self.base_folder = os.path.join(os.getenv('LOCALAPPDATA'), "EncryptMe")
