# tests/conftest.py
import pytest
from tests.config import \
    ServiceTestingConfig, GameClassTestingConfig, apiClassTestConfig
from flask import Flask


@pytest.fixture
def service_game_service():
    return ServiceTestingConfig.GAME_SERVICE


@pytest.fixture
def game_class_test_class():
    return GameClassTestingConfig.GAME_CLASS


@pytest.fixture
def api_bp_test_class():
    return apiClassTestConfig().ROUTE_CLASS


def create_app():
    app = Flask(__name__)
    app.config.from_object(apiClassTestConfig)
    app.register_blueprint(apiClassTestConfig.ROUTE_CLASS,
                           url_prefix="/api")
    return app


@pytest.fixture
def client():
    app = create_app()
    # Reset the GAME_SERVICE before each test
    app.config['GAME_SERVICE'].games = dict()
    return app.test_client()
