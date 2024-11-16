from fastapi import FastAPI

from app.controllers import (
    auth_controller,
    user_controller,
    waste_controller,
)

app = FastAPI(
    root_path="/api/v1",
)

# Public routes
app.include_router(
    auth_controller.router,
)
app.include_router(
    user_controller.router,
)
app.include_router(
    waste_controller.router,
)
