from flask import Flask

import auth
import roles

app = Flask(__name__)

app.register_blueprint(auth.bp)
app.register_blueprint(roles.bp)


if __name__ == '__main__':
    app.run()