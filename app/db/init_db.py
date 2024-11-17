# from pymongo.database import Database
#
# from app.db.session import engine
# from app.models.users import User
# from app.services.auths import get_password_hash
# from app.config import get_settings
#
#
# async def init_db() -> None:
#     user = await engine.find_one(User, {"email": get_settings().first_super_user})
#     if not user:
#         # Create user auth
#         user_in = User(
#             email=get_settings().first_super_user,
#             hashed_password=get_password_hash(get_settings().first_super_user_password),
#             first_name="Super",
#             last_name="User",
#             is_active=True,
#             is_superuser=True,
#         )
#         await engine.save(User, user_in)
