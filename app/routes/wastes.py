from fastapi import APIRouter, Depends

from app.middlewares.check_role import RoleChecker
from app.middlewares.verify_token import verify_jwt_token
from app.utils.enums import RoleEnum

router = APIRouter(
    prefix="/wastes",
    tags=["Wastes"],
    dependencies=[
        Depends(verify_jwt_token),
        Depends(RoleChecker(
            allowed_roles=[
                RoleEnum.member.lower(),
                RoleEnum.admin.lower()
            ])
        )
    ],
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
