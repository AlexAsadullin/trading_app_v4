from sqlalchemy import Select, select

from dal.interfaces import IManyFetcher, IOneFetcher
from domain.models.tokens import Token


class GetTokenByIdFetcher(IOneFetcher[Token]):
    def _build_query(self, token_id: int, user_id: int) -> Select:
        return select(Token).where(Token.id == token_id, Token.user_id == user_id)


class GetAllUserTokensFetcher(IManyFetcher[Token]):
    def _build_query(self, user_id: int) -> Select:
        return select(Token).where(Token.user_id == user_id).order_by(Token.date_added.desc())


class GetTokenByPlatformFetcher(IOneFetcher[Token]):
    def _build_query(self, user_id: int, platform: str) -> Select:
        return select(Token).where(Token.user_id == user_id, Token.platform == platform)
