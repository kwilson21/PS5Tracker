from typing import Dict

from fastapi import FastAPI
from fastapi import status
from fastapi.exceptions import HTTPException
from starlette.responses import JSONResponse
from starlette.responses import RedirectResponse

from app.db.models import create_tables
from app.db.models import drop_tables
from app.exceptions import NotAuthenticatedException
from app.exceptions import ValidationError
from app.routes import retailers
from app.routes import users
from app.rq.scheduler import clear_all_jobs
from app.rq.scheduler import schedule_periodic_jobs

app = FastAPI()
app.include_router(retailers.router)
app.include_router(users.router)


@app.exception_handler(NotAuthenticatedException)
async def not_authenticated_handler(req, exc) -> RedirectResponse:
    return RedirectResponse(url="/users/login")


@app.exception_handler(ValidationError)
async def validation_error_handler(req, exc) -> HTTPException:
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=exc.msg)


@app.on_event("startup")
async def startup_event() -> None:
    clear_all_jobs()
    schedule_periodic_jobs()
    create_tables()


@app.on_event("shutdown")
async def shutdown_event() -> None:
    drop_tables()


@app.get("/")
async def root() -> Dict[str, str]:
    return {"message": "Hello World"}
