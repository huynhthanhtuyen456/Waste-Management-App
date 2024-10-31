from fastapi import Depends, FastAPI

from app.dependencies import get_query_token, get_token_header
from app.routes.public import wastes, users
from app.routes.private import admin

app = FastAPI(dependencies=[Depends(get_query_token)])

# Public routes
app.include_router(
    users.router,
    prefix="/api/v1",
)
app.include_router(
    wastes.router,
    prefix="/api/v1"
)

# Private routes
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