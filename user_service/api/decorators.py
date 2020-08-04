from aiohttp import web

from .utils import verify_token
from .db import User


def login_required(func):
    """ Allow only auth users """

    async def wrapped(self, *args, **kwargs):
        access_token = self.request.cookies.get("access")
        verify_data = verify_token(access_token)
        user_id = verify_data["user_id"]

        if verify_data["is_valid"]:
            self.request.user = await User.get_user_by_id(
                self.request.app["db_pool"], user_id
            )
        else:
            return web.HTTPUnauthorized()

        return await func(self, *args, **kwargs)

    return wrapped
