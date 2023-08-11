import argparse
from sources.models.email import Email
from sources.configurations.exit_codes import ExitCodes


def main():
    parser = argparse.ArgumentParser(description='Encrypts a file or text using a public key')
    parser.add_argument("-v", "--version", action='version', version="%(prog)s 1.0")
    parser.add_argument("-r", "--register", type=str, nargs=1, metavar="<e-mail>",
                        help="Register a new public key with a given email address")

    args = parser.parse_args()

    if args.register:
        register_new_email(args.register[0])


def register_new_email(address):
    email = Email(address)
    if not email.is_valid():
        # TODO: use gettext and _() to provide localizations
        print("Invalid e-mail format.")
        exit(ExitCodes.INVALID_EMAIL)
