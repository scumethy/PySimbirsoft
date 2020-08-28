from datetime import datetime

import httpx

from src import config


# TODO: +- create base class w/ method that create client and request to apis -+
# TODO: x- in base class create method that checks user auth from access token -x
# TODO: !- write adequate error handling -!
# TODO: -- add requests monitoring --
class ServiceAPI:
    async def send_stats(self, **kwargs):
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{config.MONITORING_URL}/api/monitoring_service/event",
                json=dict(**kwargs),
            )
            response = resp.json()
            return response

    async def do_api_request(self, method, path, **kwargs):
        async with httpx.AsyncClient() as client:
            # get statistics params
            request_timestamp = datetime.now().timestamp()
            service = path.split("/")[4]
            url = path

            # send request to service
            resp = await client.request(method, path, **kwargs)

            # get statistics params
            response_time = datetime.now().timestamp() - request_timestamp
            status_code = resp.status_code

            # add event stats
            await self.send_stats(
                request_timestamp=request_timestamp,
                service=service,
                url=url,
                status_code=status_code,
                response_time=response_time,
            )

            return resp


class UserServiceAPI(ServiceAPI):
    def __init__(self, base_url):
        self.base = base_url

    async def reg(self, username, password):
        resp = await super().do_api_request(
            method="post",
            path=f"{self.base}/api/user_service/account/register",
            data=dict(username=username, password=password),
        )
        response = resp.json()
        return response

    async def login(self, username, password):
        resp = await super().do_api_request(
            method="post",
            path=f"{self.base}/api/user_service/account/login",
            data=dict(username=username, password=password),
        )
        response = resp.json()
        return response

    async def userinfo(self, user_id):
        resp = await super().do_api_request(
            method="post",
            path=f"{self.base}/api/user_service/user/info",
            data={"user_id": user_id},
        )
        response = resp.json()
        return response

    async def logout(self, access_token, refresh_token_id):
        resp = await super().do_api_request(
            method="get",
            path=f"{self.base}/api/user_service/account/logout",
            cookies={"access": access_token},
            headers={"Authorization": refresh_token_id},
        )
        response = resp.json()
        return response

    async def refreshtokens(self, access_token, refresh_token_id):
        resp = await super().do_api_request(
            method="post",
            path=f"{self.base}/api/user_service/refreshtokens",
            data={"access": access_token},
            headers={"Authorization": refresh_token_id},
        )
        response = resp.json()
        return response

    async def verify_user(self, access_token):
        resp = await super().do_api_request(
            method="post",
            path=f"{self.base}/api/user_service/account/verify",
            data={"access": access_token},
        )
        response = resp.json()
        return response


class GoodsServiceAPI(ServiceAPI):
    def __init__(self, base_url):
        self.base = base_url

    async def add_item(self, item):
        resp = await super().do_api_request(
            method="post", path=f"{self.base}/api/goods/items/", data=item
        )
        response = resp.json()
        return response

    async def update_item(self, item, item_id):
        resp = await super().do_api_request(
            method="put", path=f"{self.base}/api/goods/items/{item_id}", data=item
        )
        response = resp.json()
        return response

    async def delete_item(self, item_id):
        resp = await super().do_api_request(
            method="delete", path=f"{self.base}/api/goods/items/{item_id}"
        )
        response = resp.json()
        return response

    async def get_full_item(self, item_id):
        resp = await super().do_api_request(
            method="get", path=f"{self.base}/api/goods/items/{item_id}"
        )
        response = resp.json()
        return response

    async def get_short_item(self, item_id):
        resp = await super().do_api_request(
            method="get", path=f"{self.base}/api/goods/items/short/{item_id}"
        )
        response = resp.json()
        return response

    async def get_all_tags(self):
        resp = await super().do_api_request(
            method="get", path=f"{self.base}/api/goods/tags/"
        )
        response = resp.json()
        return response


class MailServiceAPI(ServiceAPI):
    def __init__(self, base_url):
        self.base = base_url

    async def add_temp(self, name, text):
        resp = await super().do_api_request(
            method="post",
            path=f"{self.base}/api/mail_service/temp",
            data=dict(name=name, text=text),
        )
        response = resp.json()
        return response

    async def get_temp(self, id):
        resp = await super().do_api_request(
            method="post", path=f"{self.base}/api/mail_service/temp/{id}"
        )
        response = resp.json()
        return response
