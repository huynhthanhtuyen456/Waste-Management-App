from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.controllers import (
    auth_controller,
    user_controller,
    waste_controller,
    category_controller
)


@asynccontextmanager
async def app_init(app: FastAPI):
    app.include_router(
        auth_controller.router,
    )
    app.include_router(
        user_controller.router,
    )
    app.include_router(
        category_controller.router,
    )
    app.include_router(
        waste_controller.router,
    )
    yield



app = FastAPI(
    root_path="/api/v1",
    title=get_settings().project_name,
    lifespan=app_init
)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
