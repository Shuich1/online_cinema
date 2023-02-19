from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from flask_security.utils import hash_password
from flask_jwt_extended import create_access_token, create_refresh_token

from extensions import user_datastore


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/signup', methods=['POST'])
def signup():
    login = request.json["username"]
    password = request.json["password"]

    user = user_datastore.create_user(
        login=login,
        password=hash_password(password)
    )

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = jsonify({'refresh_token': refresh_token})

    return response, 200, headers


@bp.route('/signin')
def signin():
    return b'signin'


@bp.route('/refresh_token')
@jwt_required
def refresh_token():
    return b'refresh_token'


@bp.route('/logout', methods=["DELETE"])
@jwt_required
def logout():
    return b'logout'


@bp.route('/change')
def change():
    return b'change'


@bp.route('/history')
def history():
    return b'history'
