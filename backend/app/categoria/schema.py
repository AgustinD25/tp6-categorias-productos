from typing import Annotated

from pydantic import StringConstraints
from sqlmodel import Field, SQLModel

NombreStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class CategoriaBase(SQLModel):
    nombre: NombreStr = Field(schema_extra={"examples": ["Electrónica"]})
    descripcion: str = Field(default="", schema_extra={"examples": ["Dispositivos y accesorios"]})


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaRead(CategoriaBase):
    id: int
