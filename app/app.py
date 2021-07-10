from fastapi import FastAPI

from app.db.models import create_tables
from app.db.models import drop_tables
from app.routes import retailers
from app.rq.scheduler import schedule_periodic_jobs
from app.services.retailer_availability_subscriber import thread

app = FastAPI()
app.include_router(retailers.router)


@app.on_event("startup")
async def startup_event():
    schedule_periodic_jobs()
    drop_tables()
    create_tables()


@app.on_event("shutdown")
async def shutdown_event():
    drop_tables()
    thread.stop()


@app.get("/")
async def root():
    return {"message": "Hello World"}
