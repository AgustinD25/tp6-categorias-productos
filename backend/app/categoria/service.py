from typing import List, Optional

from fastapi import HTTPException, status
from sqlmodel import Session, delete, func, select

from app.core.database import guardar
from app.producto.model import ProductoCategoria
from .model import Categoria
from .schema import CategoriaCreate


def _validar_nombre_unico(session: Session, nombre: str, excluir_id: Optional[int] = None) -> None:
    consulta = select(Categoria).where(func.lower(Categoria.nombre) == nombre.lower())
    if excluir_id is not None:
        consulta = consulta.where(Categoria.id != excluir_id)
    if session.exec(consulta).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe una categoría con el nombre '{nombre}'",
        )


def crear(session: Session, data: CategoriaCreate) -> Categoria:
    _validar_nombre_unico(session, data.nombre)
    return guardar(session, Categoria.model_validate(data))


def obtener_todas(session: Session) -> List[Categoria]:
    return list(session.exec(select(Categoria).order_by(Categoria.id)).all())


def obtener_por_id(session: Session, id: int) -> Optional[Categoria]:
    return session.get(Categoria, id)


def actualizar(session: Session, id: int, data: CategoriaCreate) -> Optional[Categoria]:
    categoria = session.get(Categoria, id)
    if not categoria:
        return None
    _validar_nombre_unico(session, data.nombre, excluir_id=id)
    categoria.sqlmodel_update(data.model_dump())
    return guardar(session, categoria)


def eliminar(session: Session, id: int) -> bool:
    categoria = session.get(Categoria, id)
    if not categoria:
        return False
    # Primero se borran los vínculos con productos para no violar la clave foránea.
    session.exec(delete(ProductoCategoria).where(ProductoCategoria.categoria_id == id))
    session.delete(categoria)
    session.commit()
    return True
