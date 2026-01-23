from fastapi import APIRouter, Depends

from apis.dependencies import get_current_user
from apis.responses import NotFoundErrorResponse, UnauthorizedErrorResponse
from core.moex_algopack.queries.get_moex_candles_query import GetMoexCandlesQuery
from core.users.dtos import UserProfile

from .contracts import GetAllCandlesHttpRequest, GetAllCandlesHttpResponse

router = APIRouter(prefix="", tags=["MOEX AlgoPack"])


@router.post(
    "/candles",
    response_model=GetAllCandlesHttpResponse,
    responses={
        401: {"model": UnauthorizedErrorResponse},
        404: {"model": NotFoundErrorResponse},
    },
)
async def get_moex_candles(
    body: GetAllCandlesHttpRequest,
    user: UserProfile = Depends(get_current_user),
):
    query = GetMoexCandlesQuery()
    try:
        filename = await query.execute(
            user_id=user.id,
            ticker=body.ticker,
            interval=body.interval,
            date_arg=body.date,
            start_date=body.start_date,
            end_date=body.end_date,
        )
    except ValueError as e:
        # Simple error handling for empty data
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=str(e))

    return GetAllCandlesHttpResponse(
        message="Candles data saved successfully",
        filename=filename,
        source="moex_algopack",
    )
