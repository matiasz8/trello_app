from fastapi.testclient import TestClient
from fastapi import FastAPI
import pytest

from app.api.router import api_router


class BaseController:  # pylint: disable=too-few-public-methods

    @staticmethod
    @pytest.fixture(scope='function')
    def test_client():
        app = FastAPI()
        app.include_router(api_router)
        return TestClient(app)
