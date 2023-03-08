from http import HTTPStatus

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from src.utils.extensions import user_datastore, send_user_info
from src.utils.trace_functions import traced

bp = Blueprint('roles', __name__, url_prefix='/roles')


@traced()
def has_role(name: str) -> bool:
    """Функция проверки наличия роли у пользователя"""
    current_user = user_datastore.find_user(id=get_jwt_identity())
    user_roles = [role.name for role in current_user.roles]
    return name in user_roles


@bp.route('/', methods=('GET',))
@jwt_required()
def roles():
    """Просмотр всех ролей."""
    if not has_role('admin'):
        return jsonify('Access is denied'), HTTPStatus.FORBIDDEN
    all_roles = user_datastore.role_model.query.all()
    return jsonify(all_roles)


@bp.route('/role', methods=('POST', 'DELETE'))
@jwt_required()
def role():
    """Управление ролью."""

    if not has_role('admin'):
        return jsonify('Access is denied'), HTTPStatus.FORBIDDEN

    if request.method == 'POST':
        name = request.json["name"]
        _role = user_datastore.find_role(role=name)
        if _role:
            return jsonify(f'{_role} роль уже существует')
        user_datastore.create_role(name=name)
        user_datastore.commit()
        return jsonify(f'Role {name} created')

    if request.method == 'DELETE':
        name = request.json["name"]
        _role = user_datastore.find_role(role=name)
        if not _role:
            return jsonify(f'Роль {_role} отсутствует')
        user_datastore.delete(_role)
        user_datastore.commit()
        return jsonify(f'Role {name} deleted')


@bp.route('/user/<id>', methods=('GET', 'POST', 'DELETE'))
@jwt_required()
def user(id):
    """Управление пользователем."""

    if not has_role('admin'):
        return jsonify('Access is denied'), HTTPStatus.FORBIDDEN

    _user = user_datastore.find_user(id=id)
    if not _user:
        return jsonify(f'{_user} is missing')

    if request.method == 'GET':
        return jsonify(_user.roles)

    if request.method == 'POST':
        role_name = request.json["role_name"]
        _role = user_datastore.find_role(role=role_name)
        if not _role:
            return jsonify(f'Role {_role} is missing')

        user_datastore.add_role_to_user(_user, _role)
        user_datastore.commit()

        # Отправляем в movies api информацию по группам пользователя
        send_user_info(user, request.headers)

        return jsonify(f'Role {role_name} successfully added to {_user}')

    if request.method == 'DELETE':
        role_name = request.json["role_name"]
        _role = user_datastore.find_role(role=role_name)
        if not _role:
            return jsonify(f'Role {_role} is missing')

        user_datastore.remove_role_from_user(_user, _role)

        # Отправляем в movies api информацию по группам пользователя
        send_user_info(user, request.headers)

        return jsonify(f'Role {role_name} successfully removed from {_user}')
