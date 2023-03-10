import string
from datetime import datetime
from secrets import choice as secrets_choice
from typing import Tuple

import requests
from flask import Request, current_app
from flask_jwt_extended import (create_access_token,
                                create_refresh_token)
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemyUserDatastore
from src.models.auth_history import AuthHistory
from src.models.role import Role
from src.models.user import User
from src.services.database import db
from src.utils.trace_functions import traced
from user_agents import parse

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(datastore=user_datastore)
migrate = Migrate()


@traced()
def create_tokens(identity: str) -> Tuple[str, str]:
    access_token = create_access_token(identity=identity)
    refresh_token = create_refresh_token(identity=identity)
    return access_token, refresh_token


@traced()
def add_auth_history(user: User, request: Request) -> User:
    user_agent = parse(request.headers['User-Agent'])
    if user_agent.is_mobile:
        device = 'mobile'
    elif user_agent.is_tablet:
        device = 'tablet'
    elif user_agent.is_pc:
        device = 'web'
    else:
        device = 'other'

    auth_history = AuthHistory(
            user_agent=request.headers['User-Agent'],
            host=request.headers['Host'],
            auth_date=datetime.now(),
            user_device_type=device
    )

    user.auth_history.append(auth_history)

    return user


@traced()
def generate_random_string():
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets_choice(alphabet) for _ in range(16))


@traced()
def send_user_info(user: User, headers):
    info = dict(
        pk=str(user.id),
        roles=[role.name for role in user.roles]
    )
    movies_api = current_app.config['HOST_MOVIES_API']

    requests.post(
        f'{movies_api}/api/v1/signin/',
        json=info,
        headers=headers | {
            'X-Request-Id': 'auth-request'
        }
    )
