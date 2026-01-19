from fastapi import APIRouter, Depends

from apis.dependencies import get_current_user
from apis.responses import NotFoundErrorResponse, UnauthorizedErrorResponse
from core.t_tech_api.queries.get_all_candles_query import GetAllCandlesQuery
from core.users.dtos import UserProfile

from .contracts import GetAllCandlesHttpRequest, GetAllCandlesHttpResponse

router = APIRouter(prefix="", tags=["T-Tech API"])


@router.post(
    "/candles",
    response_model=GetAllCandlesHttpResponse,
    responses={
        401: {"model": UnauthorizedErrorResponse},
        404: {"model": NotFoundErrorResponse},
    },
)
async def get_all_candles(
    body: GetAllCandlesHttpRequest,
    user: UserProfile = Depends(get_current_user),
):
    query = GetAllCandlesQuery()
    filename = await query.execute(
        user_id=user.id,
        figi=body.figi,
        interval_id=body.interval_id,
        years=body.years or 0,
        weeks=body.weeks or 0,
        days=body.days or 0,
        hours=body.hours or 0,
        minutes=body.minutes or 0,
    )

    return GetAllCandlesHttpResponse(
        message="Candles data saved successfully",
        filename=filename,
        source="candles",
    )
