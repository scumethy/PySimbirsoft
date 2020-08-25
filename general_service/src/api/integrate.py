import httpx
from src import config


class UserServiceAPI:
    def __init__(self, base_url):
        self.base = base_url

    async def reg(self, username, password):
        request_data = dict(username=username, password=password)
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base}/api/auth/register", data=request_data
            )
            response = resp.json()
            return response
