from src.api.views import users, goods


# init routers to fastapi application
def put_routers(app):
    app.include_router(users.users_router, tags=["users"])
    app.include_router(goods.goods_router, tags=["goods"])
