import sys
import unittest

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec

sys.path.append("..")
from sources.core.encryption import Encryption


class AppleEncryptionTestCase(unittest.TestCase):
    def test_decryption(self):
        # load test data
        path = './apple-encryption/example/'
        with open(path + 'public_key.txt', 'rb') as file:
            bytes_public_key = file.read()
        with open(path + 'private_key.txt', 'rb') as file:
            bytes_private_key = file.read()
        with open(path + 'encrypted.txt', 'rb') as file:
            encrypted = file.read()

        # load public keys
        encryption_key_x = bytes_public_key[1:1 + Encryption.POINT_SIZE]
        encryption_key_y = bytes_public_key[1 + Encryption.POINT_SIZE:1 + Encryption.POINT_SIZE * 2]

        public_numbers = ec.EllipticCurvePublicNumbers(
            int.from_bytes(encryption_key_x, 'big'),
            int.from_bytes(encryption_key_y, 'big'),
            ec.SECP521R1()
        )

        private_numbers = ec.EllipticCurvePrivateNumbers(
            int.from_bytes(bytes_private_key[1 + Encryption.POINT_SIZE * 2:1 + Encryption.POINT_SIZE * 3], 'big'),
            public_numbers
        )

        public_key = public_numbers.public_key(default_backend())
        private_key = private_numbers.private_key(default_backend())

        encryption = Encryption()

        # test keys
        test_data = b'Hello World!'
        test_encrypted = encryption.encrypt_with_public_key(public_key, test_data)
        self.assertEqual(encryption.decrypt_with_private_key(private_key, test_encrypted), test_data)

        # test protocol
        apple_data = encryption.decrypt_with_private_key(private_key, encrypted)
        self.assertEqual(apple_data, test_data)


if __name__ == '__main__':
    unittest.main()
