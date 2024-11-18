import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.controllers import (
    auth_controller,
    user_controller,
    waste_controller,
    category_controller,
    challenge_controller,
    scoring_criteria_controller,
    instruction_controller,
    instruction_type_controller,
)
from app.middlewares.router_logging import RouterLoggingMiddleware


@asynccontextmanager
async def app_init(app: FastAPI):
    app.include_router(auth_controller.router)
    app.include_router(user_controller.router)
    app.include_router(category_controller.router)
    app.include_router(waste_controller.router)
    app.include_router(challenge_controller.router)
    app.include_router(scoring_criteria_controller.router)
    app.include_router(instruction_controller.router)
    app.include_router(instruction_type_controller.router)
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

app.add_middleware(
    RouterLoggingMiddleware,
    logger=logging.getLogger(__name__)
)
