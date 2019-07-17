"""PytSite id.gov.ua Authentication Plugin Widgets
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from plugins.widget2 import Widget


class Auth(Widget):
    def __init__(self, uid: str = None, **kwargs):
        """Init
        """
        super().__init__(uid, **kwargs)

        self.css += ' auth-id-gov-ua auth-widget'

        from ._driver import Authentication as Driver
        self._props.update({
            'driverName': Driver().name,
            'href': kwargs.get('href')
        })
