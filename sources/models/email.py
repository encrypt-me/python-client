import re


class Email:
    email: str

    def __init__(self, email):
        self.email = email

    def is_valid(self):
        return re.match(r'[^@]+@[^@]+\.[^@]+', self.email) is not None
