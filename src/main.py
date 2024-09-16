import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.api.routes import main_router
from settings.app import settings

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    _: Request, exc: RequestValidationError
):
    exc = exc.errors()[0]
    msg = (
        f"Невозможно обработать запрос."
        f" Тип: {exc['type']}, "
        f"{exc['msg']} {'->'.join(exc['loc'])}"
    )
    return JSONResponse(
        status_code=400,
        content={"reason": msg},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(_: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"reason": exc.detail},
    )


@app.exception_handler(Exception)
async def internal_server_exc_handler(_: Request, __: HTTPException):
    return JSONResponse(
        status_code=500,
        content={"reason": "Internal Server Error"},
    )


app.include_router(main_router)


if __name__ == '__main__':
    address, port = settings.SERVER_ADDRESS.split(':')
    uvicorn.run("main:app", host=address, port=int(port), reload=True)
