import json
import time

import requests

with open("secrets/raco_app.json") as f:
    secrets = json.load(f)

TOKEN_FILE = 'secrets/token.json'

class Token:
    def __init__(self, token, expires_at, refresh_token):
        self.token = token
        self.expires_at = expires_at
        self.refresh_token = refresh_token

    @classmethod
    def from_user_code(cls, user_code):
        data = get_token(user_code)
        return cls(
            data['access_token'],
            data['expires_in'] + int(time.time()),
            data['refresh_token']
        )

    @classmethod
    def from_file(cls, file):
        with open(file) as f:
            return cls(**json.load(f))

    def save_to_file(self, file):
        with open(file, 'w') as f:
            json.dump({
                'token': self.token,
                'expires_at': self.expires_at,
                'refresh_token': self.refresh_token,
            }, f)

    def validate(self):
        if time.time() + 60 > self.expires_at:
            data = refresh_token(self.refresh_token)
            self.token = data['access_token']
            self.expires_at = data['expires_in'] + int(time.time())
            self.refresh_token = data['refresh_token']

            self.save_to_file(TOKEN_FILE)


def get_token(user_code):
    body = {
        'grant_type': 'authorization_code',
        'redirect_uri': 'http://localhost:12983',
        'code': user_code,
        'client_id': secrets["client_id"],
        'client_secret': secrets["client_secret"],
    }

    r = requests.post('https://api.fib.upc.edu/v2/o/token', params=body)
    return r.json()


def refresh_token(refresh_token):
    body = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': secrets["client_id"],
        'client_secret': secrets["client_secret"],
    }

    r = requests.post('https://api.fib.upc.edu/v2/o/token', params=body)
    return r.json()


def get_announcements(token):
    token.validate()

    headers = {
        'Authorization': f'Bearer {token.token}'
    }

    r = requests.get('https://api.fib.upc.edu/v2/jo/avisos/?format=json', headers=headers)
    return r.json()


def get_deliverables(token):
    token.validate()

    headers = {
        'Authorization': f'Bearer {token.token}'
    }

    r = requests.get('https://api.fib.upc.edu/v2/jo/practiques/?format=json', headers=headers)
    return r.json()
