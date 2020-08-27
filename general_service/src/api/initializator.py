from src.api.views import users, goods
from src import config


# init routers to fastapi application
def put_routers(app):
    app.include_router(users.users_router)
    app.include_router(goods.goods_router)
