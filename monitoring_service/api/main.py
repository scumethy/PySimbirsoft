from fastapi import FastAPI

from . import db
from .views import init_app


def get_app():
    app = FastAPI(title="Monitoring service")
    db.init_app(app)
    init_app(app)
    return app
