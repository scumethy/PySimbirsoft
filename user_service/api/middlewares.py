from aiohttp import web
import user_service.api.errors as errors


def json_error(e: Exception):
    return web.json_response(
        data={"status": e.status, "error": e.__class__.__name__, "message": e.message},
    )


@web.middleware
async def error_middleware(request, handler):
    try:
        response = await handler(request)
        return response
    except errors.ServiceError as exc:
        return json_error(exc)
