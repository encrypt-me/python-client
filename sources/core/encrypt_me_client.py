import re

from sources.core.configuration import Configuration
from sources.core.encryption import Encryption
from sources.core.exceptions.invalid_email_exception import InvalidEmailException
from sources.core.exceptions.invalid_signature_exception import InvalidSignatureException
from sources.core.formatter import Formatter
from sources.core.options import Options
from sources.core.server import Server
from sources.protobuf import encrypted_message_pb2


class EncryptMeClient:
    KEY_DATA = 'data'
    KEY_EMAIL = 'email'
    KEY_SIGNATURE = 'signature'

    options: Options
    encryption: Encryption

    def __init__(self, options):
        self.options = options
        self.encryption: Encryption = Encryption(options)

    def has_valid_email(self):
        return self.is_email_valid(self.options.email)

    @staticmethod
    def is_email_valid(email):
        return re.match(r'[^@]+@[^@]+\.[^@]+', email) is not None

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

        encrypted_message = encrypted_message_pb2.EncryptedMessage()
        encrypted_data = self.encrypt_with_public_key(public_key, message)
        if self.options.signature:
            signature_email = self.options.configuration.get_key(Configuration.KEY_EMAIL)
            signature = self.sign(encrypted_data)

            # validate signature
            signature_public_pem_key = Server.get_public_key(signature_email)
            if not self.encryption.verify(encrypted_data, signature, signature_public_pem_key):
                raise InvalidSignatureException()

            encrypted_message.email = signature_email
            encrypted_message.signature = signature

        encrypted_message.data = encrypted_data
        encrypted_message_bytes = encrypted_message.SerializeToString()
        return encrypted_message_bytes

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
        encrypted_message = encrypted_message_pb2.EncryptedMessage()
        encrypted_message.ParseFromString(encrypted_bytes)

        data = self.encryption.decrypt(encrypted_message.data)
        sender = None
        if encrypted_message.signature != b'' and encrypted_message.email != '':
            signature = encrypted_message.signature
            signature_public_pem_key = Server.get_public_key(encrypted_message.email)
            if not self.encryption.verify(encrypted_message.data, signature, signature_public_pem_key):
                if not self.options.ignore_signature:
                    raise InvalidSignatureException()
            else:
                sender = encrypted_message.email

        return data, sender

    def sign(self, encrypted_data):
        registered_email = self.options.configuration.get_key(Configuration.KEY_EMAIL)
        if not self.is_email_valid(registered_email):
            raise InvalidEmailException()

        return self.encryption.sign(encrypted_data)

    def set_current_email(self):
        conf = self.options.configuration
        conf.set_key(conf.KEY_EMAIL, self.options.email)
