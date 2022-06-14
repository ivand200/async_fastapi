from typing import List, Tuple, cast

from databases import Database
from fastapi import APIRouter, status, Depends, HTTPException

from db import get_database, engine
from models.posts import (
    posts,
    comments,
    metadata
)
from schemas.posts import (
    CommentCreate,
    CommentPublic,
    PostCreate,
    PostPublic,
    PostPartialUpdate
)


router = APIRouter()

@router.on_event("startup")
async def startup():
    await get_database().connect()
    metadata.create_all(engine)


@router.on_event("shutdown")
async def shutdown():
    await get_database().disconnect()


async def get_post_or_404(id: int, database: Database = Depends(get_database)) -> PostPublic:
    select_post_query = posts.select().where(posts.c.id == id)
    raw_post = await database.fetch_one(select_post_query)

    if raw_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    select_post_comments_query = comments.select().where(comments.c.post_id == id)
    raw_comments = await database.fetch_all(select_post_comments_query)
    comments_list = [CommentPublic(**comment) for comment in raw_comments]

    return PostPublic(**raw_post, comments=comments_list)


@router.get("/test", status_code=status.HTTP_200_OK)
async def test():
    return {"Hello": "world"}


@router.get("/posts", status_code=status.HTTP_200_OK)
async def list_posts(database: Database = Depends(get_database)) -> List[PostPublic]:
    """
    Get all posts
    """
    select_query = posts.select()
    rows = await database.fetch_all(select_query)

    result = [PostPublic(**rows) for row in rows]

    return result


@router.get("/posts/{id}", response_model=PostPublic, status_code=status.HTTP_200_OK)
async def get_post(post: PostPublic = Depends(get_post_or_404)) -> PostPublic:
    """
    Get post by id
    """
    return post


@router.post("/posts", response_model=PostPublic, status_code=status.HTTP_201_CREATED)
async def create_post(post: PostCreate, database: Database = Depends(get_database)) -> PostPublic:
    """
    Create post
    """
    insert_query = posts.insert().values(post.dict())
    post_id = await database.execute(insert_query)

    post_db = await get_post_or_404(post_id, database)

    return post_db


@router.patch("/posts/{id}", response_model=PostPublic)
async def update_post(
    post_update: PostPartialUpdate,
    post: PostPublic = Depends(get_post_or_404),
    database: Database = Depends(get_database)
) -> PostPublic:
    """
    Update Post
    """
    update_query = (
        posts.update()
        .where(posts.c.id == post.id)
        .values(post_update.dict(exclude_unset=True))
    )
    post_id = await database.execute(update_query)

    post_db = await get_post_or_404(post_id, database)

    return post_db


@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post: PostPublic = Depends(get_post_or_404), database: Database = Depends(get_database)):
    """
    Delete post by id
    """
    delete_query = posts.delete().where(posts.c.id == post.id)
    await database.execute(delete_query)


@router.post("/comments", response_model=CommentPublic, status_code=status.HTTP_201_CREATED)
async def create_comment(comment: CommentCreate, database: Database = Depends(get_database)) -> CommentPublic:
    """
    Create comment
    """
    select_post_query = posts.select().where(posts.c.id == comment.post_id)
    post = await database.fetch_one(select_post_query)

    if post is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Post {id} does not exist")

    insert_query = comments.insert().values(comment.dict())
    comment_id = await database.execute(insert_query)

    select_query = comments.select().where(comments.c.id == comment_id)
    raw_comment = await database.fetch_one(select_query)

    return raw_comment
