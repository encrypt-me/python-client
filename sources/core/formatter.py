import base64
import re


class Formatter:
    HEADER = '-----ENCRYPTED WITH ENCRYPT-ME.ORG -----\n'
    FOOTER = '-----ENCRYPTED WITH ENCRYPT-ME.ORG -----'
    LINE_LENGTH = 64

    @staticmethod
    def to_base64(data: bytes):
        base64_data = base64.b64encode(data)
        lines = [base64_data[i:i + Formatter.LINE_LENGTH] for i in range(0, len(base64_data), Formatter.LINE_LENGTH)]

        return Formatter.HEADER + '\n'.join([line.decode() for line in lines]) + '\n' + Formatter.FOOTER

    @staticmethod
    def from_base64(message):
        # TODO: improve this checks
        base64_pattern = r"(?<=-----ENCRYPTED WITH ENCRYPT-ME\.ORG -----\n)[A-Za-z0-9+/=\n]+(?=\n-----ENCRYPTED WITH ENCRYPT-ME\.ORG -----)"
        base_string = re.search(base64_pattern, message).group(0)
        return base64.b64decode(base_string)
