"""PytSite id.gov.ua Authentication Plugin Forms
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from plugins.form2 import Form
from ._api import prepare_request_uri
from ._widget import Auth as AuthWidget


class SignInForm(Form):
    def __init__(self, uid: str = None, **kwargs):
        """Init
        """
        super().__init__(uid or 'auth-id-gov-ua-sign-in-form', **kwargs)

        self.add_widget(AuthWidget(href=prepare_request_uri()))
