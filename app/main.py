import http
import logging
import time

from fastapi import FastAPI
from starlette.requests import Request

from app import __version__
from app.routes.spell_helper import router as spell_helper_router
from app.utils.errors import init_exception_handlers
from app.utils.middleware import init_middleware

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

init_exception_handlers(app)
init_middleware(app)
