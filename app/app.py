from fastapi import FastAPI

from app.routes import retailers

app = FastAPI()
app.include_router(retailers.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
