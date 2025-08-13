from fastapi import APIRouter, HTTPException, Request
from models.futbol_team import FutbolTeam
from controllers.futbol_team_controller import (
    create_futbol_team,
    get_futbol_team,
    update_futbol_team,
    delete_futbol_team,
    list_futbol_teams  
)
from utils.security import validateadmin

router = APIRouter()

@router.post("/futbol_teams", response_model=FutbolTeam, tags=["⚽ Futbol Teams"])
@validateadmin
async def create_futbol_team_endpoint(request: Request, team: FutbolTeam) -> FutbolTeam:
    """Crear un nuevo equipo de fútbol"""
    return await create_futbol_team(team)

@router.get("/futbol_teams", response_model=list[FutbolTeam], tags=["⚽ Futbol Teams"])
async def list_futbol_teams_endpoint() -> list[FutbolTeam]:
    """Obtener todos los equipos de fútbol"""
    return list_futbol_teams()  

@router.get("/futbol_teams/{team_id}", response_model=FutbolTeam, tags=["⚽ Futbol Teams"])
async def get_futbol_team_endpoint(team_id: str) -> FutbolTeam:
    """Obtener un equipo de fútbol por ID"""
    return await get_futbol_team(team_id)

@router.put("/futbol_teams/{team_id}", response_model=FutbolTeam, tags=["⚽ Futbol Teams"])
@validateadmin
async def update_futbol_team_endpoint(request: Request, team_id: str, team: FutbolTeam) -> FutbolTeam:
    """Actualizar un equipo de fútbol"""
    return await update_futbol_team(team_id, team)

@router.delete("/futbol_teams/{team_id}", response_model=dict, tags=["⚽ Futbol Teams"])
@validateadmin
async def delete_futbol_team_endpoint(request: Request, team_id: str) -> dict:
    """Eliminar un equipo de fútbol"""
    return await delete_futbol_team(team_id)
