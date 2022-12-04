import http
import logging
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request

log = logging.getLogger("fastapi")
log.level = logging.INFO


def init_middleware(app: FastAPI) -> None:
    @app.middleware("http")
    async def log_request(request: Request, call_next):
        response = await call_next(request)
        log.info(
            f"REQUEST [{request.method} {request.url.path}] FROM [{request.headers.get('user-agent')} | {request.headers.get('referer')} | {request.headers.get('origin')}] RETURNED [{response.status_code} {http.HTTPStatus(response.status_code).phrase}]"
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
        allow_origins=[
            "https://localhost",
            "http://localhost",
            "http://localhost:8080",
            "http://0.0.0.0",
            "https://cors-test.codehappy.dev",
            "https://mage-api.onrender.com",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
