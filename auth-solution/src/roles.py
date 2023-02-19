from flask import Blueprint, request
from flask_jwt_extended import jwt_required


bp = Blueprint('roles', __name__, url_prefix='/roles')


@bp.route('/', methods=('GET',))
@jwt_required()
def roles():
    """Просмотр всех ролей."""
    return b'roles'


@bp.route('/role', methods=('POST', 'PUT', 'DELETE'))
def role():
    """Управление ролью."""
    if request.method == 'POST':
        # user_datastore.create_role()
        return b'role'

    if request.method == 'PUT':
        return b'role'

    if request.method == 'DELETE':
        return b'role'
    return b'ooops'


@bp.route('/user', methods=('POST', 'PUT', 'DELETE'))
def user():
    """Управление пользователем."""
    if request.method == 'POST':
        # user_datastore.add_role_to_user()
        return b'user'

    if request.method == 'PUT':
        return b'user'

    if request.method == 'DELETE':
        # user_datastore.remove_role_from_user()
        return b'user'
    return b'ooops'

