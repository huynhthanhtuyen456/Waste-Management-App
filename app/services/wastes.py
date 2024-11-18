from pydantic import ValidationError

from app.db import engine
from app.models.users import User, ScoreRank
from app.models.wastes import Waste
from app.models.scoring_criteria import ScoringCriteria
from app.services.base_service import BaseService, CreateSchemaType
from app.utils.enums import ScoreRankEnum


class WasteService(BaseService):
    async def find_wastes(self, filters: dict):
        wastes = await self.engine.find(self.model, filters)
        return wastes

    async def create(self, instance: CreateSchemaType):
        try:
            instance = self.model.model_validate(instance)
            inserted_data = await self.engine.save(instance)
            await self.calculation_score(instance)
            return inserted_data
        except (ValidationError, TypeError) as e:
            raise ValidationError(e)

    async def calculation_score(self, waste: Waste):
        user = waste.user
        challenges = waste.category.challenges
        scoring_criteria_ids = []

        for challenge in challenges:
            scoring_criteria_ids.extend(challenge.scoring_criteria)

        scoring_criteria_ids = list(set(scoring_criteria_ids))
        query = ScoringCriteria.id.in_(scoring_criteria_ids)

        scores = await self.engine.find(ScoringCriteria, query)
        sum_score = sum([score.score for score in scores])
        score = user.score + sum_score
        rank = await self.calculate_rank(score)
        print(f"{rank=}")
        user.model_update({
            "score": score,
            "rank": rank
        })
        await self.engine.save(user)

    async def calculate_rank(self, score: int) -> ScoreRank | None:
        """
        No rank < 10
        Bronze >= 10
        Silver >= 20
        Gold >= 30
        Platinum >= 40

        :param score:
        :return:
        """
        if score < 10:
            rank = None
        elif 10 <= score < 20:
            rank = ScoreRankEnum.Bronze
        elif 20 <= score < 30:
            rank = ScoreRankEnum.Silver
        elif 30 <= score < 40:
            rank = ScoreRankEnum.Gold
        elif score >= 40:
            rank = ScoreRankEnum.Gold
        else:
            rank = None
        rank = await self.engine.find_one(ScoreRank, ScoreRank.level == rank)
        return rank



waste_service = WasteService(db_model=Waste, db_engine=engine)
__all__ = ["waste_service"]
