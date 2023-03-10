import json
import typing
from enum import Enum, unique, auto

from flask import current_app, redirect, request, url_for
from rauth import OAuth2Service
from src.utils.trace_functions import traced

if typing.TYPE_CHECKING:
    from werkzeug.wrappers import Response as BaseResponse


@unique
class Provider(Enum):
    YANDEX = auto()
    YK = auto()


class OAuthSignIn:
    providers = None

    def __init__(self, provider: Provider):
        self.provider_name = provider.name
        credentials = current_app.config['OAUTH_CREDENTIALS'][self.provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

    def authorize(self) -> "BaseResponse":
        pass

    def callback(self) -> tuple:
        pass

    @traced()
    def get_callback_url(self) -> str:
        return url_for('auth.oauth_callback', provider=self.provider_name,
                       _external=True)

    @classmethod
    def get_provider(cls, provider_name: str) -> 'OAuthSignIn':
        if cls.providers is None:
            cls.providers = {}
            for provider_class in cls.__subclasses__():
                provider = provider_class()
                cls.providers[provider.provider_name] = provider
        return cls.providers[provider_name.upper()]


class YandexSignIn(OAuthSignIn):
    def __init__(self):
        super().__init__(Provider.YANDEX)
        self.service = OAuth2Service(
            name='TEST',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://oauth.yandex.ru/authorize',
            access_token_url='https://oauth.yandex.ru/token',
            base_url='https://oauth.yandex.ru/'
        )

    @traced()
    def authorize(self) -> 'BaseResponse':
        return redirect(self.service.get_authorize_url(
            scope='login:email login:info',
            response_type='code',
            redirect_uri=self.get_callback_url())
        )

    @traced()
    def callback(self) -> tuple:
        def decode_json(payload: bytes):
            return json.loads(payload.decode('utf-8'))

        if 'code' not in request.args:
            return None, None, None
        oauth_session = self.service.get_auth_session(
            data={'code': request.args['code'],
                  'grant_type': 'authorization_code',
                  'redirect_uri': self.get_callback_url()},
            decoder=decode_json
        )
        me = oauth_session.get('https://login.yandex.ru/info').json()
        return (
            me['id'],
            'yandex',
            me.get('default_email')
        )


class VKSignIn(OAuthSignIn):
    def __init__(self):
        super().__init__(Provider.YK)
        self.service = OAuth2Service(
            name='TEST',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://oauth.vk.com/authorize',
            access_token_url='https://oauth.vk.com/access_token',
            base_url='https://oauth.vk.com'
        )

    @traced()
    def authorize(self) -> 'BaseResponse':
        return redirect(self.service.get_authorize_url(
            scope='email status',
            response_type='code',
            redirect_uri=self.get_callback_url(), v='5.131')
        )

    @traced()
    def callback(self) -> tuple:
        def decode_json(payload: bytes):
            return json.loads(payload.decode('utf-8'))

        if 'code' not in request.args:
            return None, None, None
        oauth_session = self.service.get_auth_session(
            data={'code': request.args['code'],
                  'redirect_uri': self.get_callback_url()},
            decoder=decode_json
        )
        me = oauth_session.service.access_token_response.json()
        return (
            me['user_id'],
            'vk',
            me.get('email')
        )
