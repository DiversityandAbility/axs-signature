import os
from flask import Flask

from . import blueprint


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = os.environ["SECRET_KEY"]

    app.register_blueprint(blueprint.bp)

    return app
