from typing import Annotated, Optional

from fastapi import Body, Query
from pydantic import BaseModel


class GetAllCandlesHttpRequest(BaseModel):
    figi: Annotated[str, Body(..., description="FIGI identifier")]
    interval_id: Annotated[int, Body(..., description="Candle interval ID (0-16)")]
    years: Annotated[Optional[int], Body(0, description="Years to go back")]
    weeks: Annotated[Optional[int], Body(0, description="Weeks to go back")]
    days: Annotated[Optional[int], Body(0, description="Days to go back")]
    hours: Annotated[Optional[int], Body(0, description="Hours to go back")]
    minutes: Annotated[Optional[int], Body(0, description="Minutes to go back")]


class GetAllCandlesHttpResponse(BaseModel):
    message: str
    filename: str
    source: str
