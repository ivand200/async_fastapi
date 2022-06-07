from fastapi import FastAPI

from routers.posts import router as router_posts

app = FastAPI()

app.include_router(
    router_posts,
    prefix="/api/v1",
    tags=["posts"]
)
