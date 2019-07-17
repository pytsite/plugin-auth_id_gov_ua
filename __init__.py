"""PytSite id.gov.ua Authentication Plugin
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from ._api import get_client, prepare_request_uri


def plugin_load():
    from plugins import auth, auth_ui
    from . import _driver

    auth.register_auth_driver(_driver.Authentication())
    auth_ui.register_driver(_driver.UI())
