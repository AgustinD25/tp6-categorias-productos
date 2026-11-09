from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import JSON, Column
from sqlmodel import Field, Relationship, SQLModel

from .schema import ProductoBase

if TYPE_CHECKING:
    from app.categoria.model import Categoria


class ProductoCategoria(SQLModel, table=True):
    # Tabla intermedia (muchos a muchos). La clave primaria es compuesta: evita vínculos repetidos.
    producto_id: int = Field(foreign_key="producto.id", primary_key=True)
    categoria_id: int = Field(foreign_key="categoria.id", primary_key=True)


class Producto(ProductoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # Una lista de strings no es una columna SQL nativa: se guarda como JSON.
    imagen_url: List[str] = Field(default_factory=list, sa_column=Column(JSON, nullable=False))
    categorias: List["Categoria"] = Relationship(link_model=ProductoCategoria)
