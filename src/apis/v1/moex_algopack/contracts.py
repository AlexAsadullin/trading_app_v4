from datetime import date
from typing import Annotated, Optional

from fastapi import Body
from pydantic import BaseModel


class GetAllCandlesHttpRequest(BaseModel):
    ticker: Annotated[str, Body(..., description="Ticker symbol (e.g. SBER)")]
    interval: Annotated[str, Body("10m", description="Candle interval (e.g. 1m, 10m, 1h, 1D, 1W)")]
    date: Annotated[Optional[date], Body(None, description="Date to fetch data for (default: today)")]
    start_date: Annotated[Optional[date], Body(None, description="Start date for range")]
    end_date: Annotated[Optional[date], Body(None, description="End date for range")]


class GetAllCandlesHttpResponse(BaseModel):
    message: str
    filename: str
    source: str
