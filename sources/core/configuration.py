import json
import os

from sources.core.storage.storage import Storage
from sources.core.storage.storage_factory import StorageFactory


class Configuration:
    KEY_EMAIL = 'registered-email'

    storage: Storage
    json: dict

    def __init__(self):
        self.storage = StorageFactory.create()
        self.json = {}

    def load_configuration(self):
        configuration_file = self.storage.get_configuration_file_path()
        if not os.path.exists(configuration_file):
            return {}

        try:
            with open(configuration_file, 'r') as file:
                self.json = json.loads(file.read())
        except Exception:
            return {}

    def set_key(self, key, value):
        self.json[key] = value
        self.save_configuration()

    def get_key(self, key):
        return self.json[key]

    def save_configuration(self):
        configuration_file = self.storage.get_configuration_file_path()
        with open(configuration_file, 'w') as file:
            file.write(json.dumps(self.json))
        pass
