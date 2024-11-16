from datetime import timedelta

from fastapi import APIRouter, HTTPException
from starlette import status

from app.db import UserCollection
from app.models.users import Token
from app.schemas.users import UserOut, UserAuth, UserCreate
from app.utils.enums import RoleEnum
from app.utils.utils import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, \
    authenticate_user, get_user, get_password_hash

router = APIRouter()


@router.post("/token")
async def login_for_access_token(
    auth_data: UserAuth,
) -> Token:
    user = authenticate_user(auth_data.email, auth_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "email": user.email,
            "full_name": user.first_name + " " + user.last_name,
            "role": user.role
        },
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post('/register', summary="Register a new user", response_model=UserOut)
async def create_user(user_auth: UserCreate):
    # querying database to check if user already exists
    user = get_user(user_auth.email)

    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )

    user = UserCreate(
        email=user_auth.email,
        first_name=user_auth.first_name,
        last_name=user_auth.last_name,
        password=get_password_hash(user_auth.password),
    )
    user.assign_role(RoleEnum.member)
    UserCollection.insert_one(user.__dict__)

    return user