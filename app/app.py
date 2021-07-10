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

app.add_exception_handler(NotAuthenticatedException, lambda req, exc: RedirectResponse(url="users/login"))


@app.on_event("startup")
def startup_event():
    clear_all_jobs()
    schedule_periodic_jobs()
    drop_tables()
    create_tables()


@app.on_event("shutdown")
def shutdown_event():
    drop_tables()


@app.get("/")
def root() -> Dict[str, str]:
    return {"message": "Hello World"}
