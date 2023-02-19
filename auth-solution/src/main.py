from flask import Flask

from db import init_db
import auth
import roles
from extensions import init_security, init_jwt_manager


app = Flask(__name__)
app.config['SECRET_KEY'] = '45b99b19b1e840b79bff2d3227d3915d'
app.config['SECURITY_TOKEN_AUTHENTICATION_HEADER'] = 'Authorization'
app.config['SECURITY_PASSWORD_SALT'] = 'asasdasd'

init_db()

init_security(app)
init_jwt_manager(app)

app.register_blueprint(auth.bp)
app.register_blueprint(roles.bp)


if __name__ == '__main__':
    app.run(debug=True)
