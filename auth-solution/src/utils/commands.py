import click
from flask import Blueprint
from flask_security.utils import hash_password
from src.utils.extensions import user_datastore
from src.utils.trace_functions import traced

commands = Blueprint('commands', __name__)


@commands.cli.command('createsuperuser')
@click.argument('email')
@click.argument('password')
@traced()
def createsuperuser(email, password):
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
