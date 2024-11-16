from fastapi import FastAPI

from app.routes import (
    wastes,
    users,
    auths
)

app = FastAPI()

# Public routes
app.include_router(
    auths.router,
)
app.include_router(
    users.router,
    prefix="/api/v1",
)
app.include_router(
    wastes.router,
    prefix="/api/v1"
)

# Private routes
# app.include_router(
#     admin.router,
#     prefix="/api/v1/admin",
#     tags=["admin"],
#     dependencies=[Depends(get_token_header)],
#     responses={418: {"description": "I'm a teapot"}},
# )


@app.get("/")
async def root():
    return {"message": "Hello Waste Management Applications!"}
