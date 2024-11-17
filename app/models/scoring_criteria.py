from odmantic import Model


class ScoringCriteria(Model):
    criteria: str
    score: int