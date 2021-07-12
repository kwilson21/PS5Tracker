from typing import Dict

from fastapi import FastAPI
from starlette.responses import RedirectResponse

from app.db.models import create_tables
from app.db.models import drop_tables
from app.exceptions import NotAuthenticatedException
from app.routes import retailers
from app.routes import users
from app.rq.scheduler import clear_all_jobs
from app.rq.scheduler import schedule_periodic_jobs

app = FastAPI()
app.include_router(retailers.router)
app.include_router(users.router)

app.add_exception_handler(NotAuthenticatedException, lambda req, exc: RedirectResponse(url="/users/login"))


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
