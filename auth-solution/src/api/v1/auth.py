from datetime import datetime, timedelta
from http import HTTPStatus

from flask import Blueprint, jsonify, request
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt, get_jwt_identity, jwt_required,
                                decode_token, current_user)
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
        return jsonify('Пользователь уже зарегистрирован'), HTTPStatus.CONFLICT

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

    return response, HTTPStatus.CREATED, headers


@bp.route('/signin', methods=['POST'])
def signin():
    email = request.json["email"]
    password = request.json["password"]

    user = user_datastore.find_user(email=email)

    if not user:
        return jsonify('Пользователь не зарегистрирован'), HTTPStatus.UNAUTHORIZED

    if not verify_password(password, user.password):
        return jsonify('Неверный пароль'), HTTPStatus.UNAUTHORIZED

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

    return response, HTTPStatus.OK, headers


@bp.route('/refresh_token', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    user_id = get_jwt_identity()

    access_token = create_access_token(identity=user_id)
    refresh_token = create_refresh_token(identity=user_id)

    jwt_redis_refresh_tokens.set(str(user_id), refresh_token)

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = jsonify({'refresh_token': refresh_token})

    return response, HTTPStatus.OK, headers


@bp.route('/logout', methods=['GET'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)
    return jsonify(msg="Access token revoked"), HTTPStatus.OK


@bp.route('/change', methods=['PUT'])
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

    return jsonify('updated'), HTTPStatus.OK


@bp.route('/history', methods=['GET'])
@jwt_required()
def history():
    user_id = get_jwt_identity()
    user = user_datastore.find_user(id=user_id)
    return jsonify(user.auth_history), HTTPStatus.OK
