import click
from flask import Blueprint
from flask_security.utils import hash_password
from src.utils.extensions import user_datastore

bp = Blueprint('commands', __name__)


@bp.cli.command('create')
@click.argument('email')
@click.argument('password')
def create(email, password):
    if not user_datastore.find_role(role='admin'):
        user_datastore.create_role(name='admin')
    if not user_datastore.find_user(email=email):
        user_datastore.create_user(
                email=email,
                password=hash_password(password),
                roles=['admin']
        )
    user_datastore.commit()
    return 'Superuser created'
