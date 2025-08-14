from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class Shirt(BaseModel):
    id: Optional[str] = Field(
        default=None,
        description="ID único de la camiseta"
    )
    team_id: str = Field(
        description="ID del equipo de fútbol al que pertenece la camiseta"
    )
    name: str = Field(
        description="Nombre de la camiseta",
        examples=["Camiseta local 2025"]
    )
    description: str = Field(
        description="Descripción de la camiseta",
        examples=["Camiseta oficial del Real Madrid temporada 2025"]
    )
    image: str = Field(
        description="URL de la imagen de la camiseta",
        examples=["https://images.com/realmadrid2025.jpg"]
    )
    price: float = Field(
        description="Precio de la camiseta",
        gt=0
    )
    discount: Optional[float] = Field(
        description="Descuento en porcentaje (0-100)",
        ge=0,
        le=100,
        default=0,
        examples=[10, 25, 0]
    )
    size: str = Field(
        description="Talla de la camiseta",
        examples=["S", "M", "L", "XL"]
    )

    class Config:
        json_encoders = {
            ObjectId: str
        }

class DeleteMessage(BaseModel):
    message: str