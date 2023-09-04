import re

from sources.core.encryption import Encryption
from sources.core.exceptions.invalid_email_exception import InvalidEmailException
from sources.core.formatter import Formatter
from sources.core.options import Options
from sources.core.server import Server


class EncryptMeClient:
    options: Options
    encryption: Encryption

    def __init__(self, options):
        self.options = options
        self.encryption = Encryption(options)

    def has_valid_email(self):
        return re.match(r'[^@]+@[^@]+\.[^@]+', self.options.email) is not None

    def register(self):
        if not self.has_valid_email():
            raise InvalidEmailException()

        return Server.register(self.options.email, self.encryption.get_public_key_in_pem_format())

    def validate_registration(self, validation_code_encrypted):
        validation_code_bytes = self.encryption.decrypt(validation_code_encrypted)
        validation_code = validation_code_bytes.decode(Formatter.DEFAULT_ENCODING)
        return Server.validate(self.options.email, validation_code)

    def encrypt(self, message):
        if not self.has_valid_email():
            raise InvalidEmailException()

        public_key = Server.get_public_key(self.options.email)
        return self.encrypt_with_public_key(public_key, message)

    def encrypt_with_public_key(self, public_key, message):
        return self.encryption.encrypt_with_public_pem_key(public_key,
                                                           message.encode(Formatter.DEFAULT_ENCODING))

    def generate_random_public_key(self):
        return self.encryption.generate_random_public_key_pem()

    def validate_private_key(self):
        return self.encryption.validate_private_key()

    def generate_keys(self):
        self.encryption.generate_keys()

    def decrypt(self, encrypted_bytes):
        return self.encryption.decrypt(encrypted_bytes)
