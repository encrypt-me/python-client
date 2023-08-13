import argparse

from sources.core.encryption import Encryption
from sources.core.email import Email
from sources.constants.exit_codes import ExitCodes
from sources.core.formatter import Formatter
from sources.core.server import Server


def main():
    parser = argparse.ArgumentParser(description='Encrypts a file or text using a public key')
    parser.add_argument("-v", "--version", action='version', version="%(prog)s 1.0")
    parser.add_argument("-r", "--register", type=str, nargs=1, metavar="<e-mail>",
                        help="Register a new public key with a given email address")
    parser.add_argument("-e", "--encrypt", type=str, nargs=1, metavar="<e-mail>",
                        help="Encrypts input data using a public key associated with a given email address")
    parser.add_argument("-g", "--generate-keys", action='store_true',
                        help="Generate new private and public keys")
    parser.add_argument("-d", "--decrypt", action='store_true',
                        help="Decrypts input message")
    parser.add_argument("-m", "--message", nargs=1, metavar="<message>",
                        help="Input message to encrypt")

    args = parser.parse_args()

    try:
        if args.register:
            register_new_email(args.register[0])
        elif args.encrypt:
            if not args.message:
                print('Provide a message to encrypt with -m or --message option.')
                exit(ExitCodes.NO_MESSAGE_TO_ENCRYPT)
            encrypt_data(args.encrypt[0], args.message[0])
        elif args.generate_keys:
            generate_new_keys()
        elif args.decrypt:
            decrypt_data()
    except Exception as e:
        print('Unknown error: ' + str(e) + '.')
        exit(ExitCodes.UNKNOWN_ERROR)


def register_new_email(address):
    email = Email(address)
    if not email.is_valid():
        # TODO: use gettext and _() to provide localizations
        print("Invalid e-mail format.")
        exit(ExitCodes.INVALID_EMAIL)

    encryption = Encryption()

    # TODO: it should generate keys if they are not present

    print("Registration...")
    if not Server.register(email.email, encryption.get_public_key_in_pem_format()):
        print("Registration failed.")
        exit(ExitCodes.REGISTRATION_FAILED)

    print('Provide a validation code:')
    validation_code = input()
    if not Server.validate(email.email, validation_code):
        print("Validation failed.")
        exit(ExitCodes.VALIDATION_FAILED)

    print("Registration successful.")


def encrypt_data(email, message):
    public_key = Server.get_public_key(email)

    cryptography = Encryption()
    encrypted_bytes = cryptography.encrypt_with_public_pem_key(public_key, message.encode('utf-8'))

    print(Formatter.to_base64(encrypted_bytes))


def generate_new_keys():
    cryptography = Encryption()
    cryptography.generate_keys()
    print("Keys generated.")


def decrypt_data():
    print("Enter message to decrypt (it should end with a new line):")

    encrypted_message = ''
    while True:
        line = input()
        if line == '':
            break
        encrypted_message += line + "\n"

    encryption = Encryption()
    message = encryption.decrypt(Formatter.from_base64(encrypted_message))
    print(message)
