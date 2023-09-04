import argparse

from sources.constants.exit_codes import ExitCodes
from sources.core.encrypt_me_client import EncryptMeClient
from sources.core.encryption import Encryption
from sources.core.exceptions.invalid_email_exception import InvalidEmailException
from sources.core.formatter import Formatter
from sources.core.input_reader import InputReader


def main():
    parser = argparse.ArgumentParser(description='Encrypts a file or text using a public key')

    parser.add_argument("-e", "--encrypt", type=str, nargs=1, metavar="<e-mail>",
                        help="Encrypts input data using a public key associated with a given email address")
    parser.add_argument("-d", "--decrypt", action='store_true',
                        help="Decrypts input message")
    parser.add_argument("-m", "--message", nargs=1, metavar="<message>",
                        help="Input message to encrypt")

    parser.add_argument("-r", "--register", type=str, nargs=1, metavar="<e-mail>",
                        help="Register a new public key with a given email address")
    parser.add_argument("-g", "--generate-keys", action='store_true',
                        help="Generate new private and public keys")

    parser.add_argument("-v", "--version", action='version', version="%(prog)s 1.0")

    parser.add_argument("-ec", "--encrypt-with-custom-key", action='store_true',
                        help="Encrypts input data using a custom public key")
    parser.add_argument("-gpk", "--generate-random-public-key", action='store_true',
                        help="It generates random public key and prints it to the console")

    args = parser.parse_args()

    try:
        if args.generate_random_public_key:
            generate_random_public_key()
        if args.register:
            register_new_email(args.register[0])
        elif args.encrypt:
            if not args.message:
                print('Provide a message to encrypt with -m or --message option.')
                exit(ExitCodes.NO_MESSAGE_TO_ENCRYPT)
            encrypt_data_with_email(args.encrypt[0], args.message[0])
        elif args.generate_keys:
            generate_new_keys()
        elif args.decrypt:
            decrypt_message()
        elif args.encrypt_with_custom_key:
            if not args.message:
                print('Provide a message to encrypt with -m or --message option.')
                exit(ExitCodes.NO_MESSAGE_TO_ENCRYPT)
            encrypt_data_with_custom_key(args.message[0])
    except InvalidEmailException:
        fail_with_invalid_email()
    except Exception as e:
        fail_with_unknown_exception(e)


def fail_with_invalid_email():
    # TODO: use gettext and _() to provide localizations
    print("Invalid e-mail address.")
    exit(ExitCodes.INVALID_EMAIL)


def fail_with_unknown_exception(exception):
    # TODO: use gettext and _() to provide localizations
    print("Unknown error: " + str(exception))
    exit(ExitCodes.UNKNOWN_ERROR)


def register_new_email(address):
    client = EncryptMeClient(address)
    # TODO: it should generate keys if they are not present

    print("Registration...")
    if not client.register():
        print("Registration failed.")
        exit(ExitCodes.REGISTRATION_FAILED)

    print('Provide a validation message:')
    if not client.validate_registration(InputReader.read_encrypted_base64_text()):
        print("Validation failed.")
        exit(ExitCodes.VALIDATION_FAILED)

    print("Registration successful.")


def encrypt_data_with_email(email, message):
    client = EncryptMeClient(email)
    encrypted_bytes = client.encrypt(message)
    print(Formatter.to_base64(encrypted_bytes))


def encrypt_data_with_custom_key(message):
    public_key = InputReader.read_public_key()
    encrypted_bytes = Encryption().encrypt_with_public_pem_key(public_key,
                                                               message.encode(Formatter.DEFAULT_ENCODING))
    print(Formatter.to_base64(encrypted_bytes))


def generate_new_keys():
    cryptography = Encryption()
    cryptography.generate_keys()
    print("Keys generated.")


def decrypt_message():
    print("Enter encrypted data:")

    encrypted_bytes = InputReader.read_encrypted_base64_text()
    message_bytes = Encryption().decrypt(encrypted_bytes)
    message = message_bytes.decode(Formatter.DEFAULT_ENCODING)

    print("\n")
    print("-----BEGIN DECRYPTED MESSAGE-----")
    print(message)
    print("-----END DECRYPTED MESSAGE-----")


def generate_random_public_key():
    cryptography = Encryption()
    print(cryptography.generate_random_public_key_pem())
