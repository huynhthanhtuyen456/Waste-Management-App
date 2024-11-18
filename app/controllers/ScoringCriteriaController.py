from fastapi import HTTPException
from odmantic import ObjectId
from starlette import status

from app.config import settings
from app.db import engine
from app.models.scoring_criteria import ScoringCriteria
from app.routes.scoring_criteria import router
from app.schemas.scoring_challenge import ScoringCriteriaRequestModel, ScoringCriteriaResponseModel, \
    ScoringCriteriaDeleteResponseModel


@router.get('', summary="Get list of scoring criteria", response_model=list[ScoringCriteriaResponseModel])
async def list_scoring_criteria(page: int = 1, page_break: bool = False):
    offset = {"skip": page * settings.MULTI_MAX, "limit": settings.MULTI_MAX} if page_break else {}  # noqa
    scoring_criteria = await engine.find(ScoringCriteria, **offset)

    return scoring_criteria


@router.post('', summary="Create a new scoring criteria", response_model=ScoringCriteriaResponseModel)
async def create_scoring_criteria(scoring_criteria: ScoringCriteriaRequestModel):
    # querying database to check if criteria already exists
    existed_scoring_criteria = await engine.find_one(ScoringCriteria, {"criteria": scoring_criteria.criteria})

    if existed_scoring_criteria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Scoring Criteria already exist"
        )
    new_instance = ScoringCriteria(
        criteria=scoring_criteria.criteria,
        score=scoring_criteria.score,
    )
    inserted_scoring_criteria = await engine.save(new_instance)

    return inserted_scoring_criteria


@router.get('/{scoring_criteria_id}', summary="Get a new scoring criteria", response_model=ScoringCriteriaResponseModel)
async def get_scoring_criteria(
        scoring_criteria_id: ObjectId
):
    # querying database to check if scoring_criteria already exists
    existed_scoring_criteria = await engine.find_one(ScoringCriteria, {"_id": scoring_criteria_id})

    if not existed_scoring_criteria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Not found Scoring Criteria with this id={scoring_criteria_id}"
        )

    return existed_scoring_criteria

@router.put('/{scoring_criteria_id}', summary="Update a scoring criteria", response_model=ScoringCriteriaResponseModel)
async def update_scoring_criteria(
        scoring_criteria: ScoringCriteriaRequestModel,
        scoring_criteria_id: ObjectId
):
    # querying database to check if category already exists
    existed_scoring_criteria = await engine.find_one(ScoringCriteria, {"_id": scoring_criteria_id})

    if not existed_scoring_criteria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Not found scoring criteria with this id={scoring_criteria_id}"
        )

    existed_scoring_criteria.model_update(scoring_criteria)
    await engine.save(existed_scoring_criteria)

    return existed_scoring_criteria


@router.delete('/{scoring_criteria_id}', summary="Delete a scoring criteria", response_model=ScoringCriteriaDeleteResponseModel)
async def delete_scoring_criteria(
        scoring_criteria_id: ObjectId
):
    # querying database to check if challenge already exists
    existed_scoring_criteria = await engine.find_one(ScoringCriteria, {"_id": scoring_criteria_id})

    if not existed_scoring_criteria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Not found scoring criteria with this id={scoring_criteria_id}"
        )

    await engine.delete(existed_scoring_criteria)

    return ScoringCriteriaDeleteResponseModel(message=f"Scoring criteria deleted with id={scoring_criteria_id}")
