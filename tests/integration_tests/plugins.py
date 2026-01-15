from httpx import AsyncClient


class AsyncAppClient(AsyncClient):
    async def get(self, url, *args, **kwargs):
        expected_status_code = kwargs.pop("expected_status_code", 200)

        got = await super().get(url, *args, **kwargs)
        assert got.status_code == expected_status_code

        if got.status_code == 204:
            return ""

        return got.json()

    async def post(self, url, *args, **kwargs):
        expected_status_code = kwargs.pop("expected_status_code", 200)
        assert_refresh_token = kwargs.pop("assert_refresh_token", False)

        got = await super().post(url, *args, **kwargs)
        assert got.status_code == expected_status_code

        if assert_refresh_token:
            assert "refresh_token" in got.cookies

        return got.json()
