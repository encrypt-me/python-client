import os
from sources.core.storage.storage import Storage


class WindowsStorage(Storage):
    def __int__(self):
        self.base_folder = os.path.join(os.getenv('LOCALAPPDATA'), "EncryptMe")
        os.mkdir(self.base_folder)
