import hashlib
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from sources.core.exceptions.key_not_exist_exception import KeyNotExistException
from sources.core.formatter import Formatter
from sources.core.options import Options
from sources.core.storage.storage import Storage
from sources.core.storage.storage_factory import StorageFactory


class Encryption:
    POINT_SIZE = 66
    AES_SIZE = 32
    IV_SIZE = 16
    storage: Storage
    options: Options

    def __init__(self, options: Options):
        self.storage = StorageFactory.create()
        self.options = options

    def get_private_key(self):
        private_key_path = self.storage.get_private_key_path()
        if not os.path.exists(private_key_path):
            raise KeyNotExistException()

        with open(private_key_path, 'rb') as file:
            return serialization.load_pem_private_key(
                file.read(),
                password=self.options.get_password_bytes(),
            )

    def get_public_key(self):
        return self.get_private_key().public_key()

    def get_serialization_algorithm(self):
        if self.options.password is None:
            return serialization.NoEncryption()
        return serialization.BestAvailableEncryption(self.options.get_password_bytes())

    def generate_keys(self):
        private_key = ec.generate_private_key(ec.SECP521R1(), default_backend())

        keys_path = self.storage.get_keys_path()
        private_key_path = self.storage.get_private_key_path()

        private_key_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=self.get_serialization_algorithm()
        )

        if not os.path.exists(keys_path):
            os.makedirs(keys_path)

        with open(private_key_path, 'wb') as file:
            file.write(private_key_bytes)

    def self_encrypt(self, data: bytes):
        return Encryption.encrypt_with_public_key(self.get_public_key(), data)

    def decrypt(self, data: bytes):
        return Encryption.decrypt_with_private_key(self.get_private_key(), data)

    def test(self):
        data = self.self_encrypt(b'hello')
        print(self.decrypt(data))

    @classmethod
    def extract_aes_keys(cls, shared_secret, header):
        all_bytes = shared_secret + bytes([0, 0, 0, 1]) + header
        hash_object = hashlib.sha512()
        hash_object.update(all_bytes)
        derived_key = hash_object.digest()

        aes_key = derived_key[:Encryption.AES_SIZE]
        iv = derived_key[Encryption.AES_SIZE:][:Encryption.IV_SIZE]
        return aes_key, iv

    @classmethod
    def encrypt_with_public_pem_key(cls, public_pem_key, data: bytes):
        public_key_bytes = public_pem_key.encode(Formatter.DEFAULT_ENCODING)
        public_key = serialization.load_pem_public_key(
            public_key_bytes,
            backend=default_backend()
        )
        return Encryption.encrypt_with_public_key(public_key, data)

    @classmethod
    def encrypt_with_public_key(cls, public_key, data: bytes):
        encryption_key = ec.generate_private_key(ec.SECP521R1())

        shared_secret = encryption_key.exchange(ec.ECDH(), public_key)

        encryption_public_key = encryption_key.public_key()
        x_bytes = encryption_public_key.public_numbers().x.to_bytes(Encryption.POINT_SIZE, 'big')
        y_bytes = encryption_public_key.public_numbers().y.to_bytes(Encryption.POINT_SIZE, 'big')

        # add uncompressed point prefix
        header = b'\x04' + x_bytes + y_bytes
        aes_key, iv = Encryption.extract_aes_keys(shared_secret, header)

        # Encrypt the data using AES-256 in GCM mode
        cipher = AESGCM(aes_key)

        encrypted = cipher.encrypt(iv, data, None)
        return header + encrypted

    @classmethod
    def decrypt_with_private_key(cls, private_key, data: bytes):
        shift = (Encryption.POINT_SIZE * 2) + 1

        header = data[:shift]
        encryption_key_data = header[1:]
        encryption_key_x = encryption_key_data[:Encryption.POINT_SIZE]
        encryption_key_y = encryption_key_data[Encryption.POINT_SIZE:]

        encryption_key = ec.EllipticCurvePublicNumbers(
            int.from_bytes(encryption_key_x, 'big'),
            int.from_bytes(encryption_key_y, 'big'),
            ec.SECP521R1()
        ).public_key(default_backend())

        encrypted = bytes(data[shift:])

        shared_secret = private_key.exchange(ec.ECDH(), encryption_key)

        aes_key, iv = Encryption.extract_aes_keys(shared_secret, header)

        cipher = AESGCM(aes_key)
        return cipher.decrypt(iv, encrypted, None)

    def get_public_key_in_pem_format(self):
        public_key = self.get_public_key()
        return self.internal_get_public_key_in_pem_format(public_key)

    @classmethod
    def internal_get_public_key_in_pem_format(cls, public_key):
        public_key_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return public_key_bytes.decode(Formatter.DEFAULT_ENCODING)

    @classmethod
    def generate_random_public_key_pem(cls):
        private_key = ec.generate_private_key(ec.SECP521R1(), default_backend())
        return cls.internal_get_public_key_in_pem_format(private_key.public_key())

    def validate_private_key(self):
        self.get_private_key()
