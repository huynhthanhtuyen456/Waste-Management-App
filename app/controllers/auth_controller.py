from datetime import timedelta
from typing import Annotated

from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette import status

from app.config import get_settings
from app.db import engine
from app.models.roles import Role
from app.models.users import User, AccessToken
from app.routes.auths import router
from app.schemas.tokens import TokenResponseModel
from app.schemas.users import UserAuthRequestModel, UserRegisterRequestModel, UserRegisterResponseModel
from app.services import (
    auths,
    tokens, users
)
from app.utils.enums import RoleEnum


@router.post("/token")
async def obtain_token(
    auth_data: UserAuthRequestModel,
) -> TokenResponseModel:
    user = await auths.authenticate_user(auth_data.email, auth_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=get_settings().access_token_expire_minutes)
    access_token = tokens.create_access_token(
        data={
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "full_name": user.first_name + " " + user.last_name,
            "role": user.role.name
        },
        expires_delta=access_token_expires
    )
    existed_token = await engine.find_one(AccessToken, AccessToken.email == user.email)
    if existed_token:
        await engine.delete(existed_token)

    token = AccessToken(token=access_token, email=user.email)
    await engine.save(token)
    return TokenResponseModel(access_token=access_token, token_type="bearer")


@router.get("/revoke-token")
async def revoke_token(token: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]):
    token = await engine.find_one(AccessToken, {"token": token.credentials})
    if not token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token",
        )
    await engine.delete(token)
    return {"message": "Token revoked"}


@router.post('/register', summary="Register a new user", response_model=UserRegisterResponseModel)
async def register(user_auth: UserRegisterRequestModel):
    # querying database to check if user already exists
    user = await users.get_user(user_auth.email)

    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )

    role = await engine.find_one(Role, Role.name == RoleEnum.member)

    if not role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role invalid role"
        )

    user = User(
        email=user_auth.email,
        first_name=user_auth.first_name,
        last_name=user_auth.last_name,
        password=auths.get_password_hash(user_auth.password),
        is_active=True,
        is_superuser=False,
        hashed_password=auths.get_password_hash(user_auth.password),
        role=role,
    )
    user = await engine.save(user)

    return user
