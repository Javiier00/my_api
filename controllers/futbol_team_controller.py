import logging
from fastapi import HTTPException
from models.futbol_team import FutbolTeam
from utils.mongodb import get_collection
from bson import ObjectId


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_futbol_team(team: FutbolTeam) -> FutbolTeam: 
    try:
        coll = get_collection("futbol_teams") 
        team_dict = team.model_dump(exclude={"id"})
        inserted = coll.insert_one(team_dict)
        team.id = str(inserted.inserted_id)
        return team
    except Exception as e:
        logger.error(f"Error creating futbol team: {str(e)}")  
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


async def get_futbol_team(team_id: str) -> FutbolTeam:  
    try:
        coll = get_collection("futbol_teams") 
        # Convierte el ID a ObjectId
        team_data = coll.find_one({"_id": ObjectId(team_id)})  # Cambia a ObjectId
        if not team_data:
            raise HTTPException(status_code=404, detail="Futbol team not found")
        return FutbolTeam(id=str(team_data['_id']), name=team_data['name'], country=team_data['country'])  
    except Exception as e:
        logger.error(f"Error fetching futbol team: {str(e)}")  
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


async def update_futbol_team(team_id: str, team: FutbolTeam) -> FutbolTeam: 
    try:
        coll = get_collection("futbol_teams")
        team_dict = team.model_dump(exclude={"id"})  # Excluye el id del dict

        # Convierte el ID a ObjectId y actualiza el documento
        result = coll.update_one({"_id": ObjectId(team_id)}, {"$set": team_dict})

        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Futbol team not found")

        # Obtiene el documento actualizado
        updated_team_data = coll.find_one({"_id": ObjectId(team_id)})
        if not updated_team_data:
            raise HTTPException(status_code=404, detail="Futbol team not found after update")

        # Devuelve el equipo actualizado incluyendo el id
        return FutbolTeam(id=str(updated_team_data['_id']), name=updated_team_data['name'], country=updated_team_data['country'])

    except Exception as e:
        logger.error(f"Error updating futbol team: {str(e)}") 
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


async def delete_futbol_team(team_id: str) -> dict:
    try:
        coll = get_collection("futbol_teams")
        # Convierte el ID a ObjectId
        result = coll.delete_one({"_id": ObjectId(team_id)})  # Cambia a ObjectId
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Futbol team not found")
        return {"message": "Futbol team deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting futbol team: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


def list_futbol_teams() -> list[FutbolTeam]:
    try:
        coll = get_collection("futbol_teams")

        # Obtiene todos los equipos de forma sincrónica
        teams_data = list(coll.find({}))  # Convierte el cursor a lista

        if not teams_data:
            return []  # Devuelve una lista vacía si no hay equipos

        logger.info(f"Teams data: {teams_data}")

        # Convierte cada documento a objeto FutbolTeam
        return [FutbolTeam(id=str(team['_id']), name=team['name'], country=team['country']) for team in teams_data]

    except Exception as e:
        logger.error(f"Error al obtener equipos: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Error interno al obtener la lista de equipos"
        )
