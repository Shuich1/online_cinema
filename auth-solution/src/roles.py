from flask import Blueprint, request


bp = Blueprint('roles', __name__, url_prefix='/roles')


@bp.route('/', methods=('GET',))
def roles():
    """Просмотр всех ролей."""
    return b'roles'


@bp.route('/role', methods=('POST', 'PUT', 'DELETE'))
def role():
    """Управление ролью."""
    if request.method == 'POST':
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
        return b'user'

    if request.method == 'PUT':
        return b'user'

    if request.method == 'DELETE':
        return b'user'
    return b'ooops'

