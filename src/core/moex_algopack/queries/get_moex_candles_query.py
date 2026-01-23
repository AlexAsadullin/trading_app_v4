from datetime import date
from typing import Optional

import pandas as pd
from moexalgo import Ticker

from domain.services.storage import storage_service


class GetMoexCandlesQuery:
    async def execute(
        self,
        user_id: int,
        ticker: str,
        interval: str,
        date_arg: Optional[date] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> str:
        
        # Determine date range parameters for moexalgo
        # moexalgo.Ticker.candles(date=..., start=..., end=...)
        
        moex_ticker = Ticker(ticker)
        
        # Fetch candles
        # Note: moexalgo is synchronous by default, but it's lightweight HTTP requests.
        # For high concurrency, might need run_in_executor, but simple call is fine for now.
        if start_date and end_date:
            candidates = moex_ticker.candles(date=None, start=start_date, end=end_date, period=interval)
        elif date_arg:
            candidates = moex_ticker.candles(date=date_arg, period=interval)
        else:
            # Default to today simply
            from datetime import date as dt_date
            candidates = moex_ticker.candles(date=dt_date.today(), period=interval)
            
        # Candidates is an iterator or list of objects, we can convert to DataFrame
        df = pd.DataFrame(candidates)
        
        if df.empty:
            raise ValueError(f"No data found for ticker {ticker} with specified parameters")
            
        # Ensure we have common columns if possible or just dump raw
        # Typically we want: Open, Close, High, Low, Volume, Date
        # moexalgo columns: open, close, high, low, value, volume, begin, end
        
        filename = f"moex_{ticker}_{interval}_{date_arg or 'range'}.csv"
        csv_content = df.to_csv(index=False)
        csv_bytes = csv_content.encode('utf-8')
        
        source = "moex_algopack"
        
        await storage_service.put_file(
            user_id=user_id,
            source=source,
            filename=filename,
            file_data=csv_bytes,
        )

        return filename
