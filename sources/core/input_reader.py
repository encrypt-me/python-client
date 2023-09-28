import base64

from sources.core.formatter import Formatter


class InputReader:
    @staticmethod
    def read_encrypted_base64_text():
        message = ''
        can_read = False
        len_header = len(Formatter.HEADER)
        while True:
            line = input()

            if Formatter.HEADER in line:
                header_index = line.index(Formatter.HEADER)
                if not can_read:
                    line = line[header_index + len_header:]
                    if Formatter.HEADER in line:
                        message += line[:line.index(Formatter.HEADER)]
                        return base64.b64decode(message)
                    else:
                        message += line
                    can_read = True
                else:
                    message += line[:header_index]
                    return base64.b64decode(message.strip())
            else:
                message += line

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
