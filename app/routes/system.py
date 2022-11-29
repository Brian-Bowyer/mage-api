from fastapi.routing import APIRouter

router = APIRouter()


@router.get("/", include_in_schema=False)
@router.get("/ping")
async def ping():
    """Minimal route purely for testing if the server is up.

    Always returns [True] with status 200.
    This endpoint is also what is returned through accessing the base URL directly, i.e. `GET /`.
    """
    return [True]
