from fastapi import HTTPException
from odmantic import ObjectId
from starlette import status

from app.routes.challenges import router
from app.schemas.challenges import ChallengeRequestModel, ChallengeResponseModel, ChallengeDeleteResponseModel
from app.models.challenges import Challenge
from app.models.scoring_criteria import ScoringCriteria
from app.db import engine
from app.config import get_settings


@router.get('', summary="Get list of challenges", response_model=list[ChallengeResponseModel])
async def list_challenge(page: int = 1, page_break: bool = False):
    offset = {"skip": page * get_settings().MULTI_MAX, "limit": get_settings().MULTI_MAX} if page_break else {}  # noqa
    categories = await engine.find(Challenge, **offset)

    return categories


@router.post('', summary="Create a new challenge", response_model=ChallengeResponseModel)
async def create_challenge(challenge: ChallengeRequestModel):
    # querying database to check if category already exists
    existed_challenge = await engine.find_one(Challenge, {"name": challenge.name})

    if existed_challenge:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )

    if not challenge.scoring_criteria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Scoring criteria is missing"
        )

    scoring_criteria_qs = ScoringCriteria.id.in_(challenge.scoring_criteria)
    scoring_criteria_list = await engine.find(ScoringCriteria, scoring_criteria_qs)

    if not scoring_criteria_list:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Scoring criteria does not found ids={challenge.scoring_criteria}."
        )

    new_challenge = Challenge(
        name=challenge.name,
        description=challenge.description,
        difficulty_level=challenge.difficulty_level,
        scoring_criteria=challenge.scoring_criteria,
    )
    inserted_challenge = await engine.save(new_challenge)

    return inserted_challenge


@router.get('/{challenge_id}', summary="Get a challenge", response_model=ChallengeResponseModel)
async def get_a_challenge(
        challenge_id: ObjectId
):
    # querying database to check if category already exists
    existed_challenge = await engine.find_one(Challenge, {"_id": challenge_id})

    if not existed_challenge:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Not found challenge with this id={challenge_id}"
        )

    return existed_challenge

@router.put('/{challenge_id}', summary="Update a new challenge", response_model=ChallengeResponseModel)
async def update_category(
        challenge: ChallengeRequestModel,
        challenge_id: ObjectId
):
    # querying database to check if category already exists
    existed_challenge = await engine.find_one(Challenge, {"_id": challenge_id})
    update_scoring_criteria = set(challenge.scoring_criteria).difference(existed_challenge.scoring_criteria)

    if update_scoring_criteria:
        scoring_criteria_query = ScoringCriteria.id.in_(update_scoring_criteria)
        scoring_criteria_list = await engine.find(ScoringCriteria, scoring_criteria_query)
        if not scoring_criteria_list:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Scoring criteria not found with ids={update_scoring_criteria}"
            )

    challenge.scoring_criteria = list(set(existed_challenge.scoring_criteria))

    if not existed_challenge:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Not found challenge with this id={challenge_id}"
        )

    existed_challenge.model_update(challenge)
    await engine.save(existed_challenge)

    return existed_challenge


@router.delete('/{challenge_id}', summary="Delete a new challenge", response_model=ChallengeDeleteResponseModel)
async def delete_challenge(
        challenge_id: ObjectId
):
    # querying database to check if challenge already exists
    existed_challenge = await engine.find_one(Challenge, {"_id": challenge_id})

    if not existed_challenge:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Not found challenge with this id={challenge_id}"
        )

    await engine.delete(existed_challenge)

    return ChallengeDeleteResponseModel(message=f"Challenge deleted with id={challenge_id}")
