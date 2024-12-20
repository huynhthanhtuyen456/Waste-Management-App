from enum import Enum


class RoleEnum(str, Enum):
    admin = "Admin"
    member = "Member"
    moderator = "Moderator"


class ChallengeDifficultyEnum(int, Enum):
    Easy = 1
    medium = 2
    hard = 3
    VeryHard = 4


class ScoreRankEnum(str, Enum):
    Platinum = "Platinum"
    Gold = "Gold"
    Silver = "Silver"
    Bronze = "Bronze"