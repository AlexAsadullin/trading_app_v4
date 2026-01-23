from collections import defaultdict
from datetime import timedelta
from decimal import Decimal

import pandas as pd
from t_tech.invest import Client
from t_tech.invest.utils import now

from dal.fetchers.tokens import GetTokenByPlatformFetcher
from domain.enums import CandleIntervalEnum
from domain.exceptions import NotFoundError
from domain.services.encryption import decrypt_token
from domain.services.storage import storage_service


def quote_to_decimal(data):
    units_decimal = Decimal(str(data.units))
    nano_decimal = Decimal(str(data.nano)) / Decimal('1000000000')
    return units_decimal + nano_decimal


class GetAllCandlesQuery:
    async def execute(
        self,
        user_id: int,
        figi: str,
        interval_id: int,
        years: int = 0,
        weeks: int = 0,
        days: int = 0,
        hours: int = 0,
        minutes: int = 0,
    ) -> str:
        if years == 0 and weeks == 0 and days == 0 and hours == 0 and minutes == 0:
            raise ValueError("At least one time parameter must be non-zero")

        token_fetcher = GetTokenByPlatformFetcher()
        token = await token_fetcher.fetch(user_id=user_id, platform="t_tech")
        if not token:
            raise NotFoundError(entity_name="Token", entity_id="t_tech")

        decrypted_token = decrypt_token(token.token_encrypted)

        interval = CandleIntervalEnum.get_candle_interval(interval_id)
        if interval is None:
            raise ValueError(f"Invalid interval_id: {interval_id}")

        total_days = days + (years * 365) + (weeks * 7)
        from_timedelta = now() - timedelta(
            days=total_days, hours=hours, minutes=minutes
        )

        with Client(decrypted_token) as client:
            data_for_df = defaultdict(list)
            for candle in client.get_all_candles(
                figi=figi,
                from_=from_timedelta,
                to=now(),
                interval=interval,
            ):
                open_price = quote_to_decimal(candle.open)
                close_price = quote_to_decimal(candle.close)
                high_price = quote_to_decimal(candle.high)
                low_price = quote_to_decimal(candle.low)
                volume = candle.volume
                is_growing = open_price < close_price

                data_for_df['Open'].append(open_price)
                data_for_df['Close'].append(close_price)
                data_for_df['High'].append(high_price)
                data_for_df['Low'].append(low_price)
                data_for_df['Volume'].append(volume)
                data_for_df['Date'].append(candle.time.timestamp())
                data_for_df['IsGrowing'].append(is_growing)
                data_for_df['AvgOpenClose'].append(abs(open_price - close_price))
                data_for_df['DiffOpenClose'].append(abs(open_price - close_price))
                data_for_df['DiffHighLow'].append(abs(high_price - low_price))

            df = pd.DataFrame(data_for_df)
            interval_name = interval.name.replace("CANDLE_INTERVAL_", "")
            csv_content = df.to_csv(index=False)
            csv_bytes = csv_content.encode('utf-8')

            filename = f"prices_{figi}_{interval_name}.csv"
            source = "t_tech"
            
            await storage_service.put_file(
                user_id=user_id,
                source=source,
                filename=filename,
                file_data=csv_bytes,
            )

            return filename
