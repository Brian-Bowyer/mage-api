import http
import logging
import time
from typing import Callable

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request

log = logging.getLogger("fastapi")
log.level = logging.INFO


def init_middleware(app: FastAPI) -> None:
    @app.middleware("http")
    async def log_request(request: Request, call_next):
        response = await call_next(request)
        log.info(
            f"REQUEST [{request.method} {request.url.path}] FROM [{request.headers.get('user-agent')}] RETURNED [{response.status_code} {http.HTTPStatus(response.status_code).phrase}]"
        )
        return response

    @app.middleware("http")
    async def response_time(request: Request, call_next):
        start_time = time.perf_counter()
        response = await call_next(request)
        end_time = time.perf_counter()
        response.headers["X-Response-Time"] = f"{(end_time - start_time)*1000}"
        return response

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        # allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
