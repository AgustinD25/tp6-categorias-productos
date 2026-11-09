from typing import Optional

from sqlmodel import Field

from .schema import CategoriaBase


class Categoria(CategoriaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
