import argparse
import getpass

from sources.constants.exit_codes import ExitCodes
from sources.core.encrypt_me_client import EncryptMeClient
from sources.core.exceptions.invalid_email_exception import InvalidEmailException
from sources.core.exceptions.invalid_signature_exception import InvalidSignatureException
from sources.core.exceptions.key_not_exist_exception import KeyNotExistException
from sources.core.formatter import Formatter
from sources.core.input_reader import InputReader
from sources.core.options import Options


def main():
    parser = argparse.ArgumentParser(description='Encrypts a file or text using a public key')

    parser.add_argument("-e", "--encrypt", type=str, nargs=1, metavar="<e-mail>",
                        help="Encrypts input data using a public key associated with a given email address")
    parser.add_argument("-d", "--decrypt", action='store_true',
                        help="Decrypts input message")
    parser.add_argument("-m", "--message", nargs=1, metavar="<message>",
                        help="Input message to encrypt")

    parser.add_argument("-p", "--password", action='store_true',
                        help="Use password to protect private key")
    parser.add_argument("-s", "--sign", action='store_true',
                        help="Signs encrypted data with registered email address. "
                             "Email address will be added to the message header.")
    parser.add_argument("-is", "--ignore-signature", action='store_true',
                        help="Ignore signature when decrypting message")

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
        options = Options()

        is_password_required = args.register or args.decrypt or args.generate_keys or args.sign
        is_validation_required = args.register or args.decrypt or args.sign
        is_message_required = args.encrypt or args.encrypt_with_custom_key

        if args.password and is_password_required:
            options.password = ask_password()
        if args.encrypt:
            options.email = args.encrypt[0]
        if args.register:
            options.email = args.register[0]
        if args.sign:
            options.signature = True
        if args.ignore_signature:
            options.ignore_signature = True

        client = EncryptMeClient(options)
        if is_validation_required:
            validate_client(client)

        if is_message_required and not args.message:
            fail_with_no_message_exception()

        if args.generate_random_public_key:
            print(client.generate_random_public_key())
        if args.register:
            register_new_email(client)
        elif args.encrypt:
            encrypted_data = client.encrypt(args.message[0])
            print_encrypted_data(encrypted_data)
        elif args.generate_keys:
            generate_keys(client)
        elif args.decrypt:
            decrypt_message(client)
        elif args.encrypt_with_custom_key:
            encrypted_data = client.encrypt_with_public_key(InputReader.read_public_key(), args.message[0])
            print_encrypted_data(encrypted_data)
    except InvalidEmailException:
        fail_with_invalid_email()
    except KeyNotExistException:
        fail_with_no_keys_exception()
    except InvalidSignatureException:
        fail_with_invalid_signature_exception()
    except Exception as e:
        fail_with_unknown_exception(e)


def fail_with_invalid_email():
    # TODO: use gettext and _() to provide localizations
    print("Invalid e-mail address.")
    exit(ExitCodes.INVALID_EMAIL)


def fail_with_wrong_password(exception):
    print("Invalid password. " + str(exception))
    exit(ExitCodes.INVALID_PASSWORD)


def fail_with_unknown_exception(exception):
    # TODO: use gettext and _() to provide localizations
    print("Unknown error: " + str(exception))
    exit(ExitCodes.UNKNOWN_ERROR)


def fail_with_no_message_exception():
    print('Provide a message to encrypt with -m or --message option.')
    exit(ExitCodes.NO_MESSAGE_TO_ENCRYPT)


def fail_with_passwords_do_not_match():
    print("Passwords do not match.")
    exit(ExitCodes.PASSWORDS_DO_NOT_MATCH)


def fail_with_invalid_signature_exception():
    print("Signature is invalid.")
    exit(ExitCodes.NOT_KEYS)


def fail_with_no_keys_exception():
    print("Private key is not setup.")
    exit(ExitCodes.NOT_KEYS)


def register_new_email(client: EncryptMeClient):
    print("Registration...")
    if not client.register():
        print("Registration failed.")
        exit(ExitCodes.REGISTRATION_FAILED)

    print('Provide a validation message:')
    if not client.validate_registration(InputReader.read_encrypted_base64_text()):
        print("Validation failed.")
        exit(ExitCodes.VALIDATION_FAILED)

    client.set_current_email()
    print("Registration successful.")


def decrypt_message(client: EncryptMeClient):
    print("Enter encrypted data:")

    encrypted_bytes = InputReader.read_encrypted_base64_text()
    message_bytes, sender = client.decrypt(encrypted_bytes)
    message = message_bytes.decode(Formatter.DEFAULT_ENCODING)

    print("\n")
    print("-----BEGIN DECRYPTED MESSAGE-----")
    if sender is not None:
        print("Sender: " + sender)

    print(message)
    print("-----END DECRYPTED MESSAGE-----")


def generate_keys(client: EncryptMeClient):
    if client.options.password is None:
        print("Would you like to use password to protect private key? (y/n)")
        answer = input()
        if answer == 'y':
            client.options.password = ask_password()

    if client.options.password is not None:
        retype_password = getpass.getpass(prompt='Retype password: ')
        if retype_password != client.options.password:
            fail_with_passwords_do_not_match()

    client.generate_keys()


def validate_client(client: EncryptMeClient):
    try:
        client.validate_private_key()
    except KeyNotExistException:
        print("Private key not found. Would you like to generate new keys? (y/n)")
        answer = input()
        if answer == 'y':
            generate_keys(client)
        else:
            fail_with_no_keys_exception()
    except Exception as e:
        if client.options.password is None:
            client.options.password = ask_password()
            validate_client(client)
        else:
            fail_with_wrong_password(e)


def print_encrypted_data(encrypted_bytes):
    print(Formatter.to_base64(encrypted_bytes))


def ask_password():
    return getpass.getpass(prompt='Enter password: ')
