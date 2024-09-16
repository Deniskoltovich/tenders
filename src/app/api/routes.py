from fastapi import APIRouter
from starlette.responses import PlainTextResponse

from app.api.bids.views import router as bids_router
from app.api.tenders.views import router as tenders_router

main_router = APIRouter(prefix="/api")


@main_router.get("/ping")
def ping():
    return PlainTextResponse(status_code=200, content="ok")


main_router.include_router(tenders_router)
main_router.include_router(bids_router)
