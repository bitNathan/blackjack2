# tests/conftest.py
import pytest
from tests.config import *

@pytest.fixture
def service_game_service():
    return ServiceTestingConfig.GAME_SERVICE

@pytest.fixture
def game_class_test_class():
    return GameClassTestingConfig.GAME_CLASS

