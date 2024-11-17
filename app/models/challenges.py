from odmantic import Model, ObjectId


class Challenge(Model):
    name: str
    description: str
    difficulty_level: int
    scoring_criteria: list[ObjectId]
