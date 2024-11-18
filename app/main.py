import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.controllers import (
    AuthController,
    UserController,
    WasteController,
    CategoryController,
    ChallengeController,
    ScoringCriteriaController,
    InstructionController,
    InstructionTypeController,
)
from app.middlewares.router_logging import RouterLoggingMiddleware


@asynccontextmanager
async def app_init(app: FastAPI):
    app.include_router(AuthController.router)
    app.include_router(UserController.router)
    app.include_router(CategoryController.router)
    app.include_router(WasteController.router)
    app.include_router(ChallengeController.router)
    app.include_router(ScoringCriteriaController.router)
    app.include_router(InstructionController.router)
    app.include_router(InstructionTypeController.router)
    yield



app = FastAPI(
    root_path="/api/v1",
    title=settings.project_name,
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
