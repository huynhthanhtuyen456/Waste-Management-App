from fastapi import APIRouter, Depends

from app.dependencies.verify_token import verify_jwt_token

router = APIRouter(
    prefix="/wastes",
    tags=["Wastes"],
    dependencies=[Depends(verify_jwt_token)],
    responses={
        404: {
            "status": False,
            "message": "Not found",
            "data": None
        },
        403: {
            "status": False,
            "message": "Forbidden",
            "data": None
        },
    },
)
