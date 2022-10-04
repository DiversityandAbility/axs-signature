import os
from flask import Flask

from . import blueprint, comms


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ["SECRET_KEY"]
    app.config.from_pyfile("config.py")

    comms.init_app(app)

    app.register_blueprint(blueprint.bp)

    return app
