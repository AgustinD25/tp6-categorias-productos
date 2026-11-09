from typing import Annotated, List

from pydantic import StringConstraints
from sqlmodel import Field, SQLModel

from app.categoria.schema import CategoriaRead

NombreStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class ProductoBase(SQLModel):
    nombre: NombreStr = Field(schema_extra={"examples": ["Auriculares Bluetooth"]})
    descripcion: str = Field(default="", schema_extra={"examples": ["Auriculares inalámbricos"]})
    precio_base: float = Field(ge=0, schema_extra={"examples": [49999.99]})
    imagen_url: List[str] = Field(
        default_factory=list, schema_extra={"examples": [["https://ejemplo.com/foto1.jpg"]]}
    )
    disponible: bool = True


class ProductoCreate(ProductoBase):
    # Ids de categorías a vincular al crear/reemplazar el producto (opcional).
    categoria_ids: List[int] = Field(default_factory=list)


class ProductoRead(ProductoBase):
    id: int
    categorias: List[CategoriaRead] = []
