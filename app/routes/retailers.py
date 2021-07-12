from typing import List

from fastapi import APIRouter

from app.db import retailer_store
from app.models.retailer import Retailer as RetailerModel

router = APIRouter()


@router.get("/retailers/", tags=["retailers"], response_model=List[RetailerModel])
async def get_retailers():
    return retailer_store.get_all_retailer_availabilities()
