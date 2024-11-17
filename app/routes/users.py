from fastapi import APIRouter, Depends

from app.middlewares.verify_token import verify_jwt_token

router = APIRouter(
    prefix="/users",
    dependencies=[Depends(verify_jwt_token)],
    tags=["Users"]
)