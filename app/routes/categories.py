from fastapi import APIRouter, Depends

from app.dependencies.check_role import RoleChecker
from app.dependencies.verify_token import verify_jwt_token

router = APIRouter(
    prefix="/waste-categories",
    tags=["WasteCategories"],
    dependencies=[Depends(verify_jwt_token), Depends(RoleChecker(allowed_roles=["admin"]))],
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
