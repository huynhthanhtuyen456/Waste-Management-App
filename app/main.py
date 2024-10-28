from fastapi import Depends, FastAPI

from app.dependencies import get_query_token, get_token_header
from app.internal import admin
from app.routes import items, users

app = FastAPI(dependencies=[Depends(get_query_token)])


app.include_router(
    users.router,
    prefix="/api/v1",
)
app.include_router(
    items.router,
    prefix="/api/v1"
)
app.include_router(
    admin.router,
    prefix="/api/v1/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}