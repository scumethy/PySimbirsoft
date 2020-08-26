from fastapi import Request
# from urllib.parse import urlparse

from .main import get_app
from src.api import monitoring

app = get_app()


# @app.middleware("http")
# async def monitoring_middleware(request: Request, call_next):
#     print(request.base_url.hostname)
#     # resp = await monitoring.save_event()
#     response = await call_next(request)
#     return response