"""PytSite id.gov.ua Authentication Plugin Drivers
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.router import current_url
from pytsite.http import Request
from plugins import auth, auth_ui
from plugins.auth import AbstractUser
from plugins.form2 import Form
from . import _api
from ._form import SignInForm


class Authentication(auth.driver.Authentication):
    def get_name(self) -> str:
        """Get driver's name
        """
        return 'id_gov_ua'

    def get_description(self) -> str:
        """Get driver's description
        """
        return 'id.gov.ua authentication driver'

    def sign_in(self, data: dict) -> AbstractUser:
        """Authenticate an existing user
        """
        oauth_code = data.get('code')
        if not oauth_code:
            raise auth.error.AuthenticationError('No oAuth code')

        oauth_token = _api.get_access_token(oauth_code, current_url(True), data.get('state'))
        info = _api.get_user_info(oauth_token['access_token'], oauth_token['user_id'])

        email = info['email'].lower()
        if not email:
            raise auth.error.AuthenticationError('Service returned no email')

        user = auth.get_user(email)
        if not user:
            user = auth.create_user(email)

        opts = dict(user.options)
        opts.update({
            'id_gov_ua': info,
        })
        user.set_field('options', opts)

        user.set_field('first_name', info['givenname'].title())
        user.set_field('middle_name', info['middlename'].title())
        user.set_field('last_name', info['lastname'].title())
        user.set_field('phone', info['phone'])

        return user.save()


    def sign_up(self, data: dict) -> AbstractUser:
        """Register a new user
        """
        pass

    def sign_out(self, user: AbstractUser):
        """End user's session
        """
        pass


class UI(auth_ui.Driver):
    def get_name(self) -> str:
        """Get driver's name
        """
        return 'id_gov_ua'

    def get_description(self) -> str:
        """Get driver's description
        """
        return 'id.gov.ua authentication UI driver'

    def get_sign_up_form(self, request: Request, **kwargs) -> Form:
        """Get a sign up form
        """
        return self.get_sign_in_form(request, **kwargs)

    def get_sign_in_form(self, request: Request, **kwargs) -> Form:
        """Get a sign in form
        """
        return SignInForm(**kwargs)

    def get_restore_account_form(self, request: Request, **kwargs) -> Form:
        """Get an account restoration form
        """
        raise NotImplementedError('This authentication provider does not support this function')
