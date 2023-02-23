from datetime import datetime, timedelta

from flask import Blueprint, jsonify, request
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt, get_jwt_identity, jwt_required)
from flask_security.utils import hash_password, verify_password
from src.models.auth_history import AuthHistory
from src.services.redis import jwt_redis_blocklist, jwt_redis_refresh_tokens
from src.utils.extensions import jwt, user_datastore

ACCESS_EXPIRES = timedelta(hours=1)


bp = Blueprint('auth', __name__, url_prefix='/auth')


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    return token_in_redis is not None


@bp.route('/signup', methods=['POST'])
def signup():
    email = request.json["email"]
    password = request.json["password"]

    if user_datastore.find_user(email=email):
        return jsonify('Пользователь уже зарегистрирован')

    auth_history = AuthHistory(
        user_agent=request.headers['User-Agent'],
        host=request.headers['Host'],
        auth_data=datetime.now(),
    )

    new_user = user_datastore.create_user(
        email=email,
        password=hash_password(password),
    )

    new_user.auth_history.append(auth_history)
    user_datastore.commit()

    access_token = create_access_token(identity=new_user.id)
    refresh_token = create_refresh_token(identity=new_user.id)

    jwt_redis_refresh_tokens.set(str(new_user.id), refresh_token)

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = jsonify({'refresh_token': refresh_token})

    return response, 201, headers


@bp.route('/signin', methods=['POST'])
def signin():
    email = request.json["email"]
    password = request.json["password"]
    print(1)
    user = user_datastore.find_user(email=email)

    if not user:
        return jsonify('Пользователь не зарегистрирован')

    if not verify_password(password, user.password):
        return jsonify('Неверный пароль')

    auth_history = AuthHistory(
        user_agent=request.headers['User-Agent'],
        host=request.headers['Host'],
        auth_data=datetime.now(),
    )

    user.auth_history.append(auth_history)
    user_datastore.commit()

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    jwt_redis_refresh_tokens.set(str(user.id), refresh_token)
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = jsonify({'refresh_token': refresh_token})

    return response, 200, headers


@bp.route('/refresh_token', methods=['POST'])
@jwt_required()
def refresh_token():
    refresh_token = request.json['refresh_token']
    user_id = get_jwt_identity()
    redis_refresh_token = jwt_redis_refresh_tokens.get(user_id)
    if redis_refresh_token != refresh_token:
        return jsonify('Неверный refresh token'), 400

    access_token = create_access_token(identity=user_id)
    refresh_token = create_refresh_token(identity=user_id)

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = jsonify({'refresh_token': refresh_token})

    return response, 200, headers


@bp.route('/logout', methods=['DELETE'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)
    return jsonify(msg="Access token revoked")


@bp.route('/change', methods=['POST'])
@jwt_required()
def change():
    email = None
    password = None

    if 'email' in request.json:
        email = request.json["email"]

    if 'password' in request.json:
        password = request.json["password"]

    user_id = get_jwt_identity()
    user = user_datastore.find_user(id=user_id)

    if email:
        user.email = email
    if password:
        user.password = hash_password(password)

    user_datastore.commit()

    return jsonify('updated')


@bp.route('/history', methods=['GET'])
@jwt_required()
def history():
    user_id = get_jwt_identity()
    user = user_datastore.find_user(id=user_id)
    return jsonify(user.auth_history)
