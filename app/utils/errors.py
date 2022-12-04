import traceback

from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.utils.constants import DEBUG


async def handle_exception(
    request, exc, *, status_code: int = 500, message: str = "", **kwargs
) -> JSONResponse:
    """Handles all exceptions."""
    payload = dict(
        status=status_code,
        type=str(exc.__class__.__name__),
        endpoint=f"{request.method} {request.url}",
        message=message,
        extra=kwargs.get("extra", {k: kwargs[k] for k in kwargs}),
    )
    if DEBUG:
        payload["debug"] = {
            "raw_exception": repr(exc),
            "traceback": "".join(traceback.format_tb(exc.__traceback__)),
            "request_headers": str(request.headers),
        }
        if kwargs.get("debug") is not None and isinstance(kwargs["debug"], dict):
            payload["debug"] = {**payload["debug"], **kwargs["debug"]}
    return JSONResponse(status_code=status_code, content=payload)


def init_exception_handlers(app) -> None:
    @app.exception_handler(StarletteHTTPException)
    async def handle_custom_http_exception(request, exc):
        try:
            message = exc.detail.get("message")
        except AttributeError:
            message = str(exc.detail)

        return await handle_exception(
            request,
            exc,
            status_code=exc.status_code,
            message=message,
            detail=exc.detail,
        )

    @app.exception_handler(Exception)
    async def handle_fallback_exception(
        request: Request, exc: Exception
    ) -> JSONResponse:
        return await handle_exception(request, exc)
