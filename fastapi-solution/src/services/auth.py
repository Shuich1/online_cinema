import json
from http import HTTPStatus

import jsonschema
import jwt
from fastapi import Depends, Header, HTTPException
from jwt.exceptions import InvalidTokenError
from src.core.config import settings
from src.core.trace_functions import traced
from src.db.auth_storage import AuthStorage, get_auth_storage


class AuthService:
    def __init__(self, data_storage):
        self.data_storage = data_storage
    
    @traced()
    async def signin(self, header: Header, user_data: dict):
        await self.validate_header(header)

        with open('user.json', 'r') as schema_file:
            try:
                jsonschema.validate(instance=user_data, schema=json.load(schema_file))
            except jsonschema.ValidationError:
                raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)

        user_roles = json.dumps(user_data.get('roles'))

        await self.data_storage.set(user_data.get('pk'), user_roles)
        
        return HTTPStatus.OK

    @traced()
    async def validate_header(self, header):
        access_token = header.split(" ")[1]
        try:
            jwt.decode(access_token, settings.jwt_secret_key, algorithm="HS256")
        except InvalidTokenError:
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)
        
        return True


def get_auth_service(
    data_storage: AuthStorage = Depends(get_auth_storage),
) -> AuthService:
    return AuthService(data_storage)
