import http
import logging
import time

from fastapi import FastAPI
from starlette.requests import Request

from app import __version__

from .routes.ephemeral_maker import router as ephemeral_router
from .routes.spell_helper import router as spell_helper_router

log = logging.getLogger(__name__)

app = FastAPI(
    # title=APP_TITLE,
    # description=APP_DESCRIPTION,
    version=__version__,
)


@app.get("/", include_in_schema=False)
@app.get("/ping")
async def ping():
    """Minimal route purely for testing if the server is up.

    Always returns [True] with status 200.
    This endpoint is also what is returned through accessing the base URL directly, i.e. `GET /`.
    """
    return [True]


app.include_router(spell_helper_router, prefix="/spell")
app.include_router(ephemeral_router, prefix="/ephemeral")


@app.middleware("http")
async def log_request(request: Request, call_next):
    response = await call_next(request)
    log.info(
        f"REQUEST [{request.method} {request.url.path}] FROM [{request.headers.get('user-agent')}] RETURNED [{response.status_code} {http.HTTPStatus(response.status_code).phrase}]"
    )
    return response


@app.middleware("http")
async def response_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    end_time = time.time()
    response.headers["X-Response-Time"] = f"{(end_time - start_time)*1000}"
    return response
