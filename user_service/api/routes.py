from .views import Register, Login, UserInfo, RefreshTokens, LogOut


def setup_routes(app):
    app.router.add_route(
        method="POST", path="/auth/register", handler=Register, name="registration"
    )
    app.router.add_route(method="POST", path="/auth/login", handler=Login, name="login")
    app.router.add_route(
        method="POST", path="/auth/user/info", handler=UserInfo, name="info"
    )
    app.router.add_route(
        method="POST", path="/auth/refreshtokens", handler=RefreshTokens, name="tokens"
    )
    app.router.add_route(
        method="GET", path="/auth/logout", handler=LogOut, name="logout"
    )
