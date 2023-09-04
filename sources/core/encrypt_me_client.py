import re

from sources.core.encryption import Encryption
from sources.core.exceptions.invalid_email_exception import InvalidEmailException
from sources.core.formatter import Formatter
from sources.core.server import Server


class EncryptMeClient:
    email: str
    encryption: Encryption

    def __init__(self, email):
        self.email = email
        self.encryption = Encryption()

    def has_valid_email(self):
        return re.match(r'[^@]+@[^@]+\.[^@]+', self.email) is not None

    def register(self):
        if not self.has_valid_email():
            raise InvalidEmailException()

        return Server.register(self.email, self.encryption.get_public_key_in_pem_format())

    def validate_registration(self, validation_code_encrypted):
        validation_code_bytes = self.encryption.decrypt(validation_code_encrypted)
        validation_code = validation_code_bytes.decode(Formatter.DEFAULT_ENCODING)
        return Server.validate(self.email, validation_code)

    def encrypt(self, message):
        if not self.has_valid_email():
            raise InvalidEmailException()

        public_key = Server.get_public_key(self.email)
        return self.encryption.encrypt_with_public_pem_key(public_key,
                                                           message.encode(Formatter.DEFAULT_ENCODING))
