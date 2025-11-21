# app/__init__.py
from flask import Flask
import os
from app.config import *

def create_app(config_class=None):
    app = Flask(__name__)
    env = os.environ.get("FLASK_ENV", "development")
    if (env == "development"):
        app.config.from_object(DevelopmentConfig)
    else:
        raise ValueError("Specified a config object that app doesn't handle")

    from .api.routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    return app
