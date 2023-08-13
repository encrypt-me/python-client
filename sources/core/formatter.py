import base64


class Formatter:
    HEADER = '-----ENCRYPTED WITH ENCRYPT-ME.ORG-----'
    LINE_LENGTH = 64

    PUBLIC_KEY_HEADER = '-----BEGIN PUBLIC KEY-----'
    PUBLIC_KEY_FOOTER = '-----END PUBLIC KEY-----'

    @staticmethod
    def to_base64(data: bytes):
        base64_data = base64.b64encode(data)
        lines = [base64_data[i:i + Formatter.LINE_LENGTH] for i in range(0, len(base64_data), Formatter.LINE_LENGTH)]

        return Formatter.HEADER + '\n' + '\n'.join([line.decode() for line in lines]) + '\n' + Formatter.HEADER
