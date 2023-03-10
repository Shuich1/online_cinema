import jwt
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from ..core.config import settings


def decode_jwt(token: str) -> dict:
    try:
        return jwt.decode(token, settings.jwt_secret_key, algorithms=['HS256'])
    except:
        return {}


def get_user_roles(token: str):
    decoded_token_info = jwt.decode(token, settings.jwt_secret_key, algorithms=['HS256'])
    return decoded_token_info['roles']


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            decoded_jwt = decode_jwt(credentials.credentials)
            if not decoded_jwt:
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return decoded_jwt
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")
