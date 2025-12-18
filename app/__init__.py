# app/__init__.py
from flask import Flask
from flask_cors import CORS
import os
from app.config import DevelopmentConfig
from .api.routes import api_bp


def create_app(config_class=None):
    app = Flask(__name__)
    env = os.environ.get("FLASK_ENV", "development")
    if (env == "development"):
        app.config.from_object(DevelopmentConfig)
    else:
        raise ValueError("Specified a config object that app doesn't handle")

    app.register_blueprint(api_bp, url_prefix="/api")
    CORS(app, origins=app.config["CORS_ORIGINS"])

    return app
