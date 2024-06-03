from fastapi import APIRouter
from fastapi.responses import Response
from starlette.status import HTTP_200_OK

router = APIRouter()


@router.get("/health", name="health")
def health() -> Response:
    return Response(status_code=HTTP_200_OK)
