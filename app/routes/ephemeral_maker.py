from fastapi.routing import APIRouter

router = APIRouter()


@router.get("/")
def validate():
    pass
