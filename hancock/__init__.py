from flask import Flask

from . import blueprint


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile("config.py", silent=True)

    app.register_blueprint(blueprint.bp)

    return app
