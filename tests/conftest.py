import asyncio

import httpx
import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import status

from main import app
from db import get_database
from models.posts import metadata
from tests.fake_db import get_test_database, engine


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def test_client():
    app.dependency_overrides[get_database] = get_test_database
    metadata.create_all(engine)
    async with LifespanManager(app):
        async with httpx.AsyncClient(
            app=app, base_url="http://127.0.0.1:8000/api/v1"
        ) as test_client:
                yield test_client
