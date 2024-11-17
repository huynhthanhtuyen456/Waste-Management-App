from odmantic import Model, ObjectId


class Challenge(Model):
    name: str
    description: str
    difficultyLevel: int
    scoring_criteria: list[ObjectId]


class ScoringCriteria(Model):
    criteria: str
    score: int