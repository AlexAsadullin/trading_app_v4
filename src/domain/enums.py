from enum import StrEnum


class TokenErrorCode(StrEnum):
    expired = "expired"
    invalid = "invalid"


class TokenType(StrEnum):
    access_token = "access_token"
    refresh_token = "refresh_token"


class Environment(StrEnum):
    production = "production"
    staging = "staging"
    dev = "dev"
    local = "local"


class CandleIntervalEnum(int):
    UNSPECIFIED = 0
    CANDLE_INTERVAL_5_SEC = 1
    CANDLE_INTERVAL_10_SEC = 2
    CANDLE_INTERVAL_30_SEC = 3
    CANDLE_INTERVAL_1_MIN = 4
    CANDLE_INTERVAL_2_MIN = 5
    CANDLE_INTERVAL_3_MIN = 6
    CANDLE_INTERVAL_5_MIN = 7
    CANDLE_INTERVAL_10_MIN = 8
    CANDLE_INTERVAL_15_MIN = 9
    CANDLE_INTERVAL_30_MIN = 10
    CANDLE_INTERVAL_HOUR = 11
    CANDLE_INTERVAL_2_HOUR = 12
    CANDLE_INTERVAL_4_HOUR = 13
    CANDLE_INTERVAL_DAY = 14
    CANDLE_INTERVAL_WEEK = 15
    CANDLE_INTERVAL_MONTH = 16

    @classmethod
    def get_candle_interval(cls, interval_id: int):
        from t_tech.invest import CandleInterval
        
        mapping = {
            0: CandleInterval.CANDLE_INTERVAL_UNSPECIFIED,
            1: CandleInterval.CANDLE_INTERVAL_5_SEC,
            2: CandleInterval.CANDLE_INTERVAL_10_SEC,
            3: CandleInterval.CANDLE_INTERVAL_30_SEC,
            4: CandleInterval.CANDLE_INTERVAL_1_MIN,
            5: CandleInterval.CANDLE_INTERVAL_2_MIN,
            6: CandleInterval.CANDLE_INTERVAL_3_MIN,
            7: CandleInterval.CANDLE_INTERVAL_5_MIN,
            8: CandleInterval.CANDLE_INTERVAL_10_MIN,
            9: CandleInterval.CANDLE_INTERVAL_15_MIN,
            10: CandleInterval.CANDLE_INTERVAL_30_MIN,
            11: CandleInterval.CANDLE_INTERVAL_HOUR,
            12: CandleInterval.CANDLE_INTERVAL_2_HOUR,
            13: CandleInterval.CANDLE_INTERVAL_4_HOUR,
            14: CandleInterval.CANDLE_INTERVAL_DAY,
            15: CandleInterval.CANDLE_INTERVAL_WEEK,
            16: CandleInterval.CANDLE_INTERVAL_MONTH,
        }
        return mapping.get(interval_id)


class StorageSource(StrEnum):
    t-bank = "t-bank"

