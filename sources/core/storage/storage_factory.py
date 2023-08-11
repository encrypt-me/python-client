from sources.core.storage.unix_storage import UnixStorage


class StorageFactory:
    @classmethod
    def create(cls):
        return UnixStorage()
