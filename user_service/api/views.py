import secrets
from jose import jwt
from aiohttp import web

from .db import User
from .redis import save_pair, del_pair, check_key_redis, set_ttl
from .utils import get_unique_uuid, generate_jwt
from .decorators import login_required
from user_service.config import config


class LogOut(web.View):
    @login_required
    async def get(self):
        refresh_token_id = self.request.headers["Authorization"]
        await del_pair(self.request.app["redis_pool"], refresh_token_id)
        return web.Response(text="Logout was successful!")


class Login(web.View):
    async def post(self):
        data = await self.request.post()
        username = data.get("username")
        password = data.get("pass")

        # check username and password
        user = await User.verify_user_data(
            self.request.app["db_pool"], username, password
        )
        if user is None:
            raise web.HTTPUnauthorized()

        # generate tokens
        jwt_token = generate_jwt(user["id"])
        refresh_token = secrets.token_hex(32)
        refresh_token_uuid = get_unique_uuid()

        # save refresh token in redis and set 30 days ttl (2592000 seconds)
        await save_pair(
            self.request.app["redis_pool"], refresh_token_uuid, refresh_token
        )
        await set_ttl(
            self.request.app["redis_pool"], refresh_token_uuid, 30 * 24 * 60 * 60
        )

        # set sesstions cookie
        response = web.Response()
        response.set_cookie("access", jwt_token)
        response.set_cookie("refresh", refresh_token_uuid)
        response.text = "Login was successful!"

        return response


class Register(web.View):
    async def post(self):
        body = await self.request.post()
        username = body.get("username")
        password = body.get("pass")

        await User.add_user(self.request.app["db_pool"], username, password)

        return web.Response(text="Registration done!")


class UserInfo(web.View):
    @login_required
    async def post(self):
        return web.json_response(self.request.user)


class RefreshTokens(web.View):
    async def post(self):
        refresh_token_id = self.request.headers["Authorization"]
        body = await self.request.post()
        access_token = body.get("access")
        access_token_payload = jwt.decode(
            access_token,
            config.jwt_secret,
            algorithms=config.jwt_algo,
            options={"verify_exp": False},
        )

        if await check_key_redis(self.request.app["redis_pool"], refresh_token_id):
            jwt_token = generate_jwt(access_token_payload["user_id"])
            new_refresh_token = secrets.token_hex(32)
            new_refresh_token_uuid = get_unique_uuid()

            await del_pair(self.request.app["redis_pool"], refresh_token_id)
            await save_pair(
                self.request.app["redis_pool"],
                new_refresh_token_uuid,
                new_refresh_token,
            )
            await set_ttl(self.request.app["redis_pool"], new_refresh_token_uuid, 60)

            response = web.Response()
            response.set_cookie("access", jwt_token)
            response.set_cookie("refresh", new_refresh_token_uuid)
            response.text = "Tokens refreshed!"
            return response
        else:
            return web.HTTPUnauthorized(text="Invalid refresh token")
