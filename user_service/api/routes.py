from .views import Register, Login, UserInfo, RefreshTokens, LogOut, VerifyUser


def setup_routes(app):
    app.router.add_route(
        method="POST",
        path="/api/user_service/account/register",
        handler=Register,
        name="registration",
    )
    app.router.add_route(
        method="POST",
        path="/api/user_service/account/login",
        handler=Login,
        name="login",
    )
    app.router.add_route(
        method="POST", path="/api/user_service/user/info", handler=UserInfo, name="info"
    )
    app.router.add_route(
        method="POST",
        path="/api/user_service/refreshtokens",
        handler=RefreshTokens,
        name="tokens",
    )
    app.router.add_route(
        method="GET",
        path="/api/user_service/account/logout",
        handler=LogOut,
        name="logout",
    )
    app.router.add_route(
        method="POST",
        path="/api/user_service/account/verify",
        handler=VerifyUser,
        name="verify",
    )
