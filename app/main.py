from fastapi import FastAPI

from app import __version__

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
