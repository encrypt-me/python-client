import os

from sources.core.storage.unix_storage import UnixStorage
from sources.core.storage.windows_storage import WindowsStorage


class StorageFactory:
    @staticmethod
    def create():
        # if windows
        if os.name == 'nt':
            return WindowsStorage()
        else:
            return UnixStorage()
