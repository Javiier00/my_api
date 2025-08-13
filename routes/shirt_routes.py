from fastapi import APIRouter, Request
from controllers.shirt_controller import create_shirt, get_shirt, update_shirt, delete_shirt, list_shirts
from models.shirt import Shirt, DeleteMessage

from utils.security import validateadmin

router = APIRouter()



@router.post("/shirts", response_model=Shirt,tags=["👕 Shirt"])
@validateadmin
async def create_new_shirt(request: Request, shirt: Shirt) -> Shirt:
    return await create_shirt(shirt)





@router.get("/shirts/{shirt_id}", response_model=Shirt, tags=["👕 Shirt"])
async def read_shirt(shirt_id: str):
    return await get_shirt(shirt_id)





@router.put("/shirts/{shirt_id}", response_model=Shirt, tags=["👕 Shirt"])
@validateadmin
async def update_existing_shirt(request: Request, shirt_id: str, shirt: Shirt)-> Shirt:
    return await update_shirt(shirt_id, shirt)





@router.delete("/shirts/{shirt_id}", response_model= DeleteMessage, tags=["👕 Shirt"])
@validateadmin
async def remove_shirt(request: Request, shirt_id: str)-> Shirt:
    return await delete_shirt(shirt_id)





@router.get("/shirts", response_model=list[Shirt], tags=["👕 Shirt"])
async def read_shirts():
    return await list_shirts()
