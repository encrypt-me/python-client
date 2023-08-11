import os


class Storage:
    base_folder: str

    def get_keys_path(self):
        return os.path.join(self.base_folder, 'keys')

    def get_private_key_path(self):
        return os.path.join(self.get_keys_path(), 'private.pem')
