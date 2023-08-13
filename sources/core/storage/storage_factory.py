import os

from sources.core.storage.unix_storage import UnixStorage


class StorageFactory:
    @staticmethod
    def create():
        # if windows
        if os.name == 'nt':
            raise NotImplementedError("Windows is not supported yet.")
        else:
            return UnixStorage()
