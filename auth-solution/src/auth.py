from datetime import timedelta, datetime, timezone

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from flask_security.utils import hash_password, verify_password, verify_hash
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies
import redis


from .extensions import user_datastore, jwt


ACCESS_EXPIRES = timedelta(hours=1)

jwt_redis_blocklist = redis.StrictRedis(
    host="localhost", port=6379, db=0, decode_responses=True
)

bp = Blueprint('auth', __name__, url_prefix='/auth')


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None


# TODO: Заменить на обновление в headers
# @bp.after_request
# def refresh_expiring_jwts(response):
#     try:
#         exp_timestamp = get_jwt()["exp"]
#         now = datetime.now(timezone.utc)
#         target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
#         if target_timestamp > exp_timestamp:
#             access_token = create_access_token(identity=get_jwt_identity())
#             set_access_cookies(response, access_token)
#         return response
#     except (RuntimeError, KeyError):
#         # Case where there is not a valid JWT. Just return the original response
#         return response


@bp.route('/signup', methods=['POST'])
def signup():
    login = request.json["username"]
    password = request.json["password"]

    user = user_datastore.create_user(
        login=login,
        password=hash_password(password)
    )
    user_datastore.commit()

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = jsonify({'refresh_token': refresh_token})

    return response, 200, headers


@bp.route('/signin')
def signin():
    login = request.json["username"]
    password = request.json["password"]

    user = user_datastore.find_user(login=login)

    if not user:
        return jsonify('Пользователь не зарегистрирован')

    if not verify_password(password, user.password):
        return jsonify('Не верный пароль')

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = jsonify({'refresh_token': refresh_token})

    return response, 200, headers


@bp.route('/refresh_token')
@jwt_required()
def refresh_token():
    return b'refresh_token'


@bp.route('/logout', methods=['DELETE'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)
    return jsonify(msg="Access token revoked")


@bp.route('/change')
def change():
    return b'change'


@bp.route('/history')
def history():
    return b'history'
