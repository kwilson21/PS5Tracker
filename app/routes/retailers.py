from fastapi import APIRouter

from app.db import retailer_store

router = APIRouter()


@router.get("/retailers/", tags=["retailers"])
async def get_retailers():
    return retailer_store.get_all_retailer_availabilities()
