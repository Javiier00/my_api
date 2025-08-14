import logging
from fastapi import HTTPException
from models.shirt import Shirt, DeleteMessage
from utils.mongodb import get_collection
from bson import ObjectId

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)




async def create_shirt(shirt: Shirt) -> Shirt:
    try:
        coll = get_collection("shirts")
        shirt_dict = shirt.dict(exclude={"id"})  # Usar dict() en lugar de model_dump()

        # Validaciones básicas del producto
        if shirt.price <= 0:
            raise HTTPException(status_code=400, detail="El precio debe ser mayor que cero.")
        if shirt.discount < 0 or shirt.discount > 100:
            raise HTTPException(status_code=400, detail="El descuento debe estar entre 0 y 100.")
        valid_sizes = ['S', 'M', 'L', 'XL']
        if shirt.size not in valid_sizes:
            raise HTTPException(status_code=400, detail="Talla no válida.")

        # Verificación de existencia del equipo
        team_exists = get_collection("futbol_teams").find_one({"_id": ObjectId(shirt.team_id)})
        if not team_exists:
            raise HTTPException(status_code=404, detail="El equipo no existe.")

        # Inserción en la base de datos
        inserted = coll.insert_one(shirt_dict)
        shirt.id = str(inserted.inserted_id)
        return shirt
        
    except Exception as e:
        logger.error(f"Error creating shirt: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")




async def get_shirt(shirt_id: str) -> Shirt:
    try:
        coll = get_collection("shirts")
        shirt_data = coll.find_one({"_id": ObjectId(shirt_id)})
        if not shirt_data:
            raise HTTPException(status_code=404, detail="Camiseta encontrada pero sin modificaciones en sus valores.")
        return Shirt(id=str(shirt_data['_id']), **shirt_data)  # Desempaqueta el resto de los campos
    except Exception as e:
        logger.error(f"Error fetching shirt: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")




async def update_shirt(shirt_id: str, shirt: Shirt) -> Shirt:
    try:
        coll = get_collection("shirts")
        shirt_dict = shirt.dict(exclude={"id"})
        # Validaciones
        if shirt.price <= 0:
            raise HTTPException(status_code=400, detail="El precio debe ser mayor que cero.")
        if shirt.discount < 0 or shirt.discount > 100:
            raise HTTPException(status_code=400, detail="El descuento debe estar entre 0 y 100.")
        valid_sizes = ['S', 'M', 'L', 'XL']
        if shirt.size not in valid_sizes:
            raise HTTPException(status_code=400, detail="Talla no válida.")
        # Verificar que el equipo existe
        team_exists = get_collection("futbol_teams").find_one({"_id": ObjectId(shirt.team_id)})
        if not team_exists:
            raise HTTPException(status_code=404, detail="El equipo no existe.")
        # Actualizar el documento
        result = coll.update_one({"_id": ObjectId(shirt_id)}, {"$set": shirt_dict})  
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Camiseta no encontrada.")
        updated_shirt_data = coll.find_one({"_id": ObjectId(shirt_id)})  
        return Shirt(id=str(updated_shirt_data['_id']), **updated_shirt_data)
    except Exception as e:
        logger.error(f"Error updating shirt: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


async def delete_shirt(shirt_id: str) -> DeleteMessage:
    try:
        coll = get_collection("shirts")
        
        result = coll.delete_one({"_id": ObjectId(shirt_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Shirt not found")
        
        return {"message": "Shirt deleted successfully"}
    
    except Exception as e:
        logger.error(f"Error deleting Shirt: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


async def list_shirts() -> list[Shirt]:
    try:
        coll = get_collection("shirts")
        shirts_data = list(coll.find({}))
        if not shirts_data:
            return []

        logger.info(f"Shirts data: {shirts_data}")
        return [Shirt(id=str(shirt['_id']), **shirt) for shirt in shirts_data]
    except Exception as e:
        logger.error(f"Error al obtener camisetas: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error interno al obtener la lista de camisetas")
