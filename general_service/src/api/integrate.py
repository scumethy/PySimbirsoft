import httpx

from src import config
from src.api.schemas import ItemModel


# TODO: create base class w/ method that create client and request to apis
# TODO: in base class create method that checks user auth from access token
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

    async def userinfo(self, user_id):
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base}/api/auth/user/info", data={"user_id": user_id}
            )
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

    async def verify_user(self, access_token):
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{self.base}/api/auth/verify", data={"access": access_token}
            )
            response = resp.json()
            return response


class GoodsServiceAPI:
    def __init__(self, base_url):
        self.base = base_url

    async def add_item(self, item):
        request_data = item
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{self.base}/api/items/", data=request_data)
            response = resp.json()
            return response

    async def update_item(self, item, item_id):
        request_data = item
        async with httpx.AsyncClient() as client:
            resp = await client.put(
                f"{self.base}/api/items/{item_id}", data=request_data
            )
            response = resp.json()
            return response

    async def delete_item(self, item_id):
        async with httpx.AsyncClient() as client:
            resp = await client.delete(f"{self.base}/api/items/{item_id}")
            response = resp.json()
            return response

    async def get_full_item(self, item_id):
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{self.base}/api/items/{item_id}")
            response = resp.json()
            return response

    async def get_short_item(self, item_id):
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{self.base}/api/items/short/{item_id}")
            response = resp.json()
            return response

    async def get_all_tags(self):
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{self.base}/api/tags/")
            response = resp.json()
            return response


class MailServiceAPI:
    def __init__(self, base_url):
        self.base = base_url

    async def add_temp(self, name, text):
        request_data = dict(name=name, text=text)
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{self.base}/api/temp", data=request_data)
            response = resp.json()
            return response

    async def get_temp(self, id):
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{self.base}/api/temp/{id}")
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
