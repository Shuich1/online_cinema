from flask import Blueprint


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/signup')
def signup():
    return b'signup'


@bp.route('/signin')
def signin():
    return b'signin'


@bp.route('/refresh_token')
def refresh_token():
    return b'refresh_token'


@bp.route('/logout')
def logout():
    return b'logout'


@bp.route('/change')
def change():
    return b'change'


@bp.route('/history')
def history():
    return b'history'
