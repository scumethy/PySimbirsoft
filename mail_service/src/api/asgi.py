from .main import get_app
import asyncio
from src.api.listener import listen

app = get_app()


@app.on_event("startup")
def startup():
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(listen(loop))
