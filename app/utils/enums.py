from enum import Enum


class RoleEnum(str, Enum):
    admin = "Admin"
    member = "Member"
    moderator = "Moderator"
