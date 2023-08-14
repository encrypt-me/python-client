import os
from sources.core.storage.storage import Storage


class WindowsStorage(Storage):
    def __int__(self):
        self.base_folder = os.path.join(os.getenv('APPDATA'), 'EncryptMe')
        if not os.path.isdir(self.base_folder):
            os.mkdir(self.base_folder)
