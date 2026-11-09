from typing import List, Optional

from fastapi import HTTPException, status
from sqlmodel import Session, delete, func, select

from app.categoria.model import Categoria
from app.core.database import guardar
from .model import Producto, ProductoCategoria
from .schema import ProductoCreate


def _validar_nombre_unico(session: Session, nombre: str, excluir_id: Optional[int] = None) -> None:
    consulta = select(Producto).where(func.lower(Producto.nombre) == nombre.lower())
    if excluir_id is not None:
        consulta = consulta.where(Producto.id != excluir_id)
    if session.exec(consulta).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe un producto con el nombre '{nombre}'",
        )


def _cargar_categorias(session: Session, ids: List[int]) -> List[Categoria]:
    ids_unicos = list(dict.fromkeys(ids))
    if not ids_unicos:
        return []
    encontradas = list(session.exec(select(Categoria).where(Categoria.id.in_(ids_unicos))).all())
    faltantes = set(ids_unicos) - {c.id for c in encontradas}
    if faltantes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categorías inexistentes: {sorted(faltantes)}",
        )
    return encontradas


def crear(session: Session, data: ProductoCreate) -> Producto:
    _validar_nombre_unico(session, data.nombre)
    categorias = _cargar_categorias(session, data.categoria_ids)
    producto = Producto.model_validate(data.model_dump(exclude={"categoria_ids"}))
    producto.categorias = categorias
    return guardar(session, producto)


def obtener_todos(session: Session, skip: int, limit: int) -> List[Producto]:
    consulta = select(Producto).order_by(Producto.id).offset(skip).limit(limit)
    return list(session.exec(consulta).all())


def obtener_por_id(session: Session, id: int) -> Optional[Producto]:
    return session.get(Producto, id)


def actualizar(session: Session, id: int, data: ProductoCreate) -> Optional[Producto]:
    producto = session.get(Producto, id)
    if not producto:
        return None
    _validar_nombre_unico(session, data.nombre, excluir_id=id)
    categorias = _cargar_categorias(session, data.categoria_ids)
    producto.sqlmodel_update(data.model_dump(exclude={"categoria_ids"}))
    producto.categorias = categorias
    return guardar(session, producto)


def eliminar(session: Session, id: int) -> bool:
    producto = session.get(Producto, id)
    if not producto:
        return False
    session.exec(delete(ProductoCategoria).where(ProductoCategoria.producto_id == id))
    session.delete(producto)
    session.commit()
    return True


# ---- Relación Producto <-> Categoría ----

def vincular_categoria(session: Session, producto_id: int, categoria_id: int) -> Producto:
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Producto no encontrado")
    categoria = session.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Categoría no encontrada")
    if categoria in producto.categorias:
        raise HTTPException(status.HTTP_409_CONFLICT, "El producto ya tiene esa categoría")
    producto.categorias.append(categoria)
    return guardar(session, producto)


def desvincular_categoria(session: Session, producto_id: int, categoria_id: int) -> None:
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Producto no encontrado")
    categoria = next((c for c in producto.categorias if c.id == categoria_id), None)
    if not categoria:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "El producto no tiene esa categoría")
    producto.categorias.remove(categoria)
    guardar(session, producto)
