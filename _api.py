"""PytSite id.gov.ua Authentication Plugin API Functions
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import requests
import json
from oauthlib.oauth2 import WebApplicationClient
from pytsite import reg, router, util

HOST = 'id.gov.ua'
REQUEST_URI = f'https://{HOST}'
GET_ACCESS_TOKEN_URI = f'https://{HOST}/get-access-token'
GET_USER_INFO_URI = f'https://{HOST}/get-user-info'


def get_client_id() -> str:
    client_id = reg.get('auth_id_gov_ua.client_id')
    if not client_id:
        raise RuntimeError('auth_id_gov_ua.client_id configuration parameter is not defined')

    return client_id


def get_client_secret() -> str:
    client_secret = reg.get('auth_id_gov_ua.client_secret')
    if not client_secret:
        raise RuntimeError('auth_id_gov_ua.client_secret configuration parameter is not defined')

    return client_secret


def get_client(code: str = None) -> WebApplicationClient:
    """Get oAuth2 client instance
    """
    return WebApplicationClient(get_client_id(), code)


def prepare_request_uri(state: str = None, redirect_uri: str = None, auth_type: str = 'dig_sign,bank_id,mobile_id'):
    """Prepare oAuth2 request URI
    """
    state = state or util.random_str()
    redirect_uri = redirect_uri or router.current_url()

    return get_client().prepare_request_uri(REQUEST_URI, redirect_uri, state=state, auth_type=auth_type)


def get_access_token(code: str, redirect_uri: str, state: str, ) -> dict:
    """Exchange code to access token
    """
    d = get_client(code).prepare_token_request(GET_ACCESS_TOKEN_URI, redirect_url=redirect_uri,
                                               state=state, client_secret=get_client_secret())

    req_uri = f'{d[0]}?{d[2]}'
    resp = requests.get(req_uri)
    if not resp.ok:
        raise RuntimeError(f'Error while querying {req_uri}: {resp.content.decode()}')

    return json.loads(resp.content)


def get_user_info(access_token: str, user_id: int) -> dict:
    req_uri = router.url(GET_USER_INFO_URI, query={'access_token': access_token, 'user_id': user_id})
    resp = requests.get(req_uri)

    if not resp.ok:
        raise RuntimeError(f'Error while querying {req_uri}: {resp.content.decode()}')

    return json.loads(resp.content)
