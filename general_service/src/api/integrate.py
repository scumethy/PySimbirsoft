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

    async def login(self, username, password):
        request_data = dict(username=username, password=password)
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{self.base}/api/auth/login", data=request_data)
            response = resp.json()
            return response

    async def userinfo(self, access_token):
        async with httpx.AsyncClient() as client:
            print(access_token)
            resp = await client.post(
                f"{self.base}/api/auth/user/info",
                cookies=dict(access=access_token)
            )
            print(resp)
            print(resp.content)
            response = resp.json()
            return response

    async def logout(self, access_token, refresh_token_id):
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{self.base}/api/auth/logout",
                cookies={"access": access_token},
                headers={"Authorization": refresh_token_id},
            )
            response = resp.json()
            return response

    async def refreshtokens(self, access_token, refresh_token_id):
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base}/api/auth/refreshtokens",
                data={"access": access_token},
                headers={"Authorization": refresh_token_id},
            )
            response = resp.json()
            return response


class MonitoringServiceAPI:
    def __init__(self, base_url):
        self.base = base_url

    async def save_event(self, **event):
        request_data = dict()
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{self.base}/api/event", data=request_data)
            response = resp.json()
            return response
