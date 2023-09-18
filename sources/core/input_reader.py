import base64

from sources.core.formatter import Formatter


class InputReader:
    @staticmethod
    def read_encrypted_base64_text():
        message = ''
        can_read = False
        while True:
            line = input().strip()

            if line.count(Formatter.HEADER) == 2:
                while line[:len(Formatter.HEADER)] != Formatter.HEADER:
                    line = line[1:]
                while line[-len(Formatter.HEADER):] != Formatter.HEADER:
                    line = line[:-1]
                message += line[len(Formatter.HEADER):-len(Formatter.HEADER)]
                return base64.b64decode(message)
            else:
                if (Formatter.HEADER in line and can_read is False or len(line) > len(Formatter.HEADER) and
                        Formatter.HEADER in line and can_read is False):
                    while line[:len(Formatter.HEADER)] != Formatter.HEADER:
                        line = line[1:]
                    message += line[len(Formatter.HEADER):]
                    line = line[:len(Formatter.HEADER)]
                else:
                    if (Formatter.HEADER in line and line[-len(Formatter.HEADER):] != Formatter.HEADER or len(line) >
                            len(Formatter.HEADER) and Formatter.HEADER in line):
                        while line[-len(Formatter.HEADER):] != Formatter.HEADER:
                            line = line[:-1]
                        message += line[:-len(Formatter.HEADER)]
                        line = line[-len(Formatter.HEADER):]

            if line[:39] == Formatter.HEADER:
                if len(line) > 39 and line[-39:] == Formatter.HEADER:
                    message += line[39:-39]
                    line = Formatter.HEADER
                    can_read = True
                else:
                    message += line[39:]

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
