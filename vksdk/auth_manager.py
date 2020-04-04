import logging
import requests
import json
from .vk_settings import AUTH_CLIENT


class Credentials:

    def __init__(self, dict_):
        self._dict = dict_
        self.access_token = dict_.get('access_token')
        self.user_id = dict_.get('user_id')
        self.expires_in = dict_.get('expires_in')

    def __str__(self):
        return str(self._dict)

    def session_serialize(self):
        return self._dict


class Auth:

    @staticmethod
    def make_url(redirect_uri, scope_list, display):
        """
            return url for auth method
        """
        if display not in ('page', 'popup'):
            logging.error('Field display may contain only "page" or "popup" value')
        url = f'https://oauth.vk.com/authorize?client_id={AUTH_CLIENT.client_id}&' \
              f'scope={",".join(scope_list)}&' \
              f'display={display}&' \
              f'redirect_uri={redirect_uri}&' \
              f'response_type=code&' \
              f'v=5.103'
        return url

    @staticmethod
    def auth(redirect_uri, code):
        """
            return json info with access_token, id_token
        """
        response = requests.get('https://oauth.vk.com/access_token',
                                params={'client_id': AUTH_CLIENT.client_id,
                                        'client_secret': AUTH_CLIENT.client_secret,
                                        'redirect_uri': redirect_uri,
                                        'code': code})
        return Credentials(response.json())

    @staticmethod
    def get_user_info(user_ids, credentials, name_case='', fields=''):
        name_case = f'name_case={name_case}'
        fields = f'fields={",".join(fields)}'
        response = requests.get(
            f'https://api.vk.com/method/users.get?user_ids={",".join(user_ids)}&'
            f'fields={",".join(fields)}&'
            f'{name_case}&'
            f'access_token={credentials.access_token}&'
            f'v=5.103')
        return response
