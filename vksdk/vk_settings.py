import json


class ClientCredentials:

    def __init__(self, file_path):
        with open(file_path) as file:
            self._json = json.load(file)
            self.client_id = self._json.get('client_id')
            self.client_secret = self._json.get('client_secret')
            self.community_key = self._json.get('community_key')


AUTH_CLIENT = ClientCredentials('vk_app.json')
#AUTH_CLIENT = 'test'

CALLBACK_URL = 'callback_url/'
CALLBACK_GROUPID = '192788863'

