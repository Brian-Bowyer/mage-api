import http
import logging
import time

from fastapi import FastAPI
from starlette.requests import Request

from app import __version__
from app.routes.spell_helper import router as spell_helper_router
from app.routes.system import router as system_router
from app.utils.errors import init_exception_handlers
from app.utils.middleware import init_middleware

log = logging.getLogger(__name__)

app = FastAPI(
    # title=APP_TITLE,
    # description=APP_DESCRIPTION,
    version=__version__,
)

app.include_router(system_router)
app.include_router(spell_helper_router, prefix="/spell")

init_middleware(app)
init_exception_handlers(app)
