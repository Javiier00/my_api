from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class FutbolTeam(BaseModel):
    id: Optional[str] = Field(
        default=None,
        description="ID único del equipo de fútbol"
    )
    name: str = Field(
        description="Nombre del equipo de fútbol",
        examples=["Real Madrid"]
    )
    country: str = Field(
        description="País al que pertenece el equipo de fútbol",
        examples=["España"]
    )

    class Config:
        # Esto permite que Pydantic maneje ObjectId de MongoDB
        json_encoders = {
            ObjectId: str
        }