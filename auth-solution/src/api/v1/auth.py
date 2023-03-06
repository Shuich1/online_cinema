from datetime import timedelta
from http import HTTPStatus

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from flask_security.utils import hash_password, verify_password
from src.models.auth_history import AuthHistory
from src.services.redis import jwt_redis_blocklist, jwt_redis_refresh_tokens
from src.utils.extensions import (add_auth_history, create_tokens, jwt,
                                  user_datastore)
from src.utils.trace_functions import traced

ACCESS_EXPIRES = timedelta(hours=1)


bp = Blueprint('auth', __name__, url_prefix='/auth')


@jwt.token_in_blocklist_loader
@traced
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

    new_user = user_datastore.create_user(
        email=email,
        password=hash_password(password),
    )

    new_user = add_auth_history(new_user, request)
    user_datastore.commit()

    access_token, refresh_token = create_tokens(identity=new_user.id)

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

    user = add_auth_history(user, request)
    user_datastore.commit()

    access_token, refresh_token = create_tokens(identity=user.id)

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

    access_token, refresh_token = create_tokens(identity=user_id)

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


@bp.route('/history/<int:page>', methods=['GET'])
@jwt_required()
def history(page=1):
    per_page = 10
    user_id = get_jwt_identity()
    _history = AuthHistory.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page, error_out=False)
    return jsonify(_history.items), HTTPStatus.OK
