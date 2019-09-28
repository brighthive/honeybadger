import os

from flask import Flask
from uuid import uuid4
from honeybadger import mci, auth, referrals, home
from honeybadger.config import ConfigurationFactory


def create_app():
    config = ConfigurationFactory.from_env()
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=ConfigurationFactory.generate_secret_key(),
        ENV=config.environment,
        DEBUG=config.debug,
        TESTING=config.testing)
    app.register_blueprint(home.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(mci.bp)
    app.register_blueprint(referrals.bp)

    return app
