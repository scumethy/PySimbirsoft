from .views import Register, Login, UserInfo, RefreshTokens, LogOut


def setup_routes(app):
    app.router.add_route(
        method="POST", path="/api/auth/register", handler=Register, name="registration"
    )
    app.router.add_route(method="POST", path="/api/auth/login", handler=Login, name="login")
    app.router.add_route(
        method="POST", path="/api/auth/user/info", handler=UserInfo, name="info"
    )
    app.router.add_route(
        method="POST", path="/api/auth/refreshtokens", handler=RefreshTokens, name="tokens"
    )
    app.router.add_route(
        method="GET", path="/api/auth/logout", handler=LogOut, name="logout"
    )
