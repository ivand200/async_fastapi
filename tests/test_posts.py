import asyncio

import pytest
import httpx
import pytest_asyncio

from fastapi import status
from schemas.posts import PostCreate, PostPublic
from models.posts import posts
from tests.fake_db import database_test


@pytest_asyncio.fixture(autouse=True, scope="module")
async def initial_posts():
    initial_posts = [
        PostCreate(title="Post 1", content="Content 1"),
        PostCreate(title="Post 2", content="Content 2"),
        PostCreate(title="Post 3", content="Content 3"),
    ]

    for post in initial_posts:
        insert = posts.insert().values(post.dict())
        post = await database_test.execute(insert)

    yield initial_posts

    for p in initial_posts:
        delete = posts.delete().where(posts.c.title == p.title)
        await database_test.execute(delete)




@pytest.mark.asyncio
async def test_hello(test_client: httpx.AsyncClient):
    response = await test_client.get("/test")
    response_body = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_body == {"Hello": "world"}


@pytest.mark.asyncio
class TestCreatePost:
    async def test_invalid(self, test_client: httpx.AsyncClient):
        payload = {"content": "test_content"}
        response = await test_client.post("/posts", json=payload)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_valid(self, test_client: httpx.AsyncClient):
        payload = {"title": "Test_title", "content": "test_content"}
        response = await test_client.post("/posts", json=payload)
        response_body = response.json()

        assert response.status_code == status.HTTP_201_CREATED
        assert response_body["title"] == "Test_title"
        assert response_body["content"] == "test_content"
        id = response_body["id"]

        response_delete = await test_client.delete(f"/posts/{id}")

        assert response_delete.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
class TestGetPost:
    async def test_not_existing(self, test_client: httpx.AsyncClient):
        response = await test_client.get("/posts/999999")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    async def test_existing(self, test_client: httpx.AsyncClient):
        test_post = await test_client.post("/posts", json={"title": "test", "content": "content"})
        test_post_body = test_post.json()
        response = await test_client.get(f"/posts/{test_post_body['id']}")

        assert response.status_code == status.HTTP_200_OK

        delete = posts.delete().where(posts.c.id == test_post_body['id'])
        await database_test.execute(delete)
