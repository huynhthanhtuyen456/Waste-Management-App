# from datetime import datetime, timezone, timedelta
# from typing import Annotated
#
# import jwt
# from fastapi import Depends, HTTPException
# from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
# from jwt import InvalidTokenError
# from passlib.context import CryptContext
# from starlette import status
#
# from app.config import get_settings
# from app.models.users import User, TokenData
# from app.db import engine
#
#
# # to get a string like this run:
# # openssl rand - hex 32
# SECRET_KEY = get_settings().secret_key
# ALGORITHM = get_settings().algorithm
# ACCESS_TOKEN_EXPIRE_MINUTES = get_settings().access_token_expire_minutes
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#
#
# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)
#
#
# def get_password_hash(password):
#     return pwd_context.hash(password)
#
#
# async def get_user(email: str):
#     user = await engine.find_one(User, User.email == email)
#     if user:
#         return user
#
#
# async def authenticate_user(email: str, password: str):
#     user = await get_user(email)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user
#
#
# def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.now(timezone.utc) + expires_delta
#     else:
#         expire = datetime.now(timezone.utc) + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt
#
#
# async def get_current_user(token: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"Authorization": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
#         email: str = payload.get("email")
#         if email is None:
#             raise credentials_exception
#         token_data = TokenData(email=email)
#     except InvalidTokenError:
#         raise credentials_exception
#     user = await get_user(email=token_data.email)
#     if user is None:
#         raise credentials_exception
#     return user
#
#
# async def get_current_active_user(
#     current_user: Annotated[User, Depends(get_current_user)],
# ):
#     if not current_user.is_active:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user