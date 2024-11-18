from fastapi import APIRouter, Depends

from app.middlewares.verify_token import verify_jwt_token
from app.middlewares.check_role import RoleChecker

router = APIRouter(
    prefix="/instruction-types",
    tags=["WasteInstructionType"],
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
