import json

from rauth import OAuth2Service
from flask import current_app, request, redirect, url_for


class OAuthSignIn:
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for('auth.oauth_callback', provider=self.provider_name,
                       _external=True)

    @classmethod
    def get_provider(cls, provider_name):
        if cls.providers is None:
            cls.providers = {}
            for provider_class in cls.__subclasses__():
                provider = provider_class()
                cls.providers[provider.provider_name] = provider
        return cls.providers[provider_name]


class YandexSignIn(OAuthSignIn):
    def __init__(self):
        super(YandexSignIn, self).__init__('yandex')
        self.service = OAuth2Service(
            name='TEST',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://oauth.yandex.ru/authorize',
            access_token_url='https://oauth.yandex.ru/token',
            base_url='https://oauth.yandex.ru/'
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='login:email login:info',
            response_type='code',
            redirect_uri=self.get_callback_url())
        )

    def callback(self):
        def decode_json(payload):
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
        super(VKSignIn, self).__init__('vk')
        self.service = OAuth2Service(
            name='TEST',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://oauth.vk.com/authorize',
            access_token_url='https://oauth.vk.com/access_token',
            base_url='https://oauth.vk.com'
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='email status',
            response_type='code',
            redirect_uri=self.get_callback_url(), v='5.131')
        )

    def callback(self):
        def decode_json(payload):
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
