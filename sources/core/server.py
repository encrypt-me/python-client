import json
import requests

from sources.constants.server_urls import ServerUrls


class Server:
    @staticmethod
    def get_headers():
        return {'Content-Type': 'application/json'}

    @staticmethod
    def register(email, public_key):
        data = {
            'email': email,
            'public_key': public_key
        }
        response = requests.post(ServerUrls.REGISTRATION_URL, headers=Server.get_headers(), data=json.dumps(data))

        return response.status_code == 200

    @staticmethod
    def validate(email, code):
        data = {
            'email': email,
            'code': code
        }
        response = requests.post(ServerUrls.VALIDATION_URL, headers=Server.get_headers(), data=json.dumps(data))

        return response.status_code == 200

    @staticmethod
    def get_public_key(email):
        data = {
            'email': email
        }
        response = requests.post(ServerUrls.GET_PUBLIC_KEY_URL, headers=Server.get_headers(), data=json.dumps(data))

        if response.status_code == 200:
            return response.json()['public_key']
