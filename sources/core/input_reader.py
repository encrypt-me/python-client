import base64

from sources.core.formatter import Formatter


class InputReader:
    @staticmethod
    def read_encrypted_base64_text():
        message = ''
        can_read = False
        while True:
            line = input()

            if line == Formatter.HEADER:
                if can_read:
                    break
                else:
                    can_read = True
                    continue

            if can_read:
                message += line

        return base64.b64decode(message)

    @staticmethod
    def read_public_key():
        can_read = False
        message = ''
        while True:
            line = input()

            if line == Formatter.PUBLIC_KEY_HEADER:
                can_read = True

            if can_read:
                message += line + '\n'

            if line == Formatter.PUBLIC_KEY_FOOTER:
                break

        return message
