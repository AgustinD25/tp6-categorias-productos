from typing import List

from fastapi import APIRouter, HTTPException, Path, Query, Response, status

from app.categoria.schema import CategoriaRead
from app.core.database import SessionDep
from . import schema, service

router = APIRouter(prefix="/productos", tags=["Productos"])

NO_ENCONTRADO = "Producto no encontrado"


@router.get("", response_model=List[schema.ProductoRead])
def listar_productos(
    session: SessionDep, skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100)
):
    return service.obtener_todos(session, skip, limit)


@router.get("/{id}", response_model=schema.ProductoRead)
def detalle_producto(session: SessionDep, id: int = Path(..., gt=0)):
    producto = service.obtener_por_id(session, id)
    if not producto:
        raise HTTPException(status.HTTP_404_NOT_FOUND, NO_ENCONTRADO)
    return producto


@router.post("", response_model=schema.ProductoRead, status_code=status.HTTP_201_CREATED)
def crear_producto(producto: schema.ProductoCreate, session: SessionDep):
    return service.crear(session, producto)


@router.put("/{id}", response_model=schema.ProductoRead)
def actualizar_producto(
    producto: schema.ProductoCreate, session: SessionDep, id: int = Path(..., gt=0)
):
    actualizado = service.actualizar(session, id, producto)
    if not actualizado:
        raise HTTPException(status.HTTP_404_NOT_FOUND, NO_ENCONTRADO)
    return actualizado


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(session: SessionDep, id: int = Path(..., gt=0)):
    if not service.eliminar(session, id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, NO_ENCONTRADO)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# ---- ProductoCategoria ----

@router.get("/{id}/categorias", response_model=List[CategoriaRead])
def categorias_del_producto(session: SessionDep, id: int = Path(..., gt=0)):
    producto = service.obtener_por_id(session, id)
    if not producto:
        raise HTTPException(status.HTTP_404_NOT_FOUND, NO_ENCONTRADO)
    return producto.categorias


@router.post(
    "/{id}/categorias/{categoria_id}",
    response_model=schema.ProductoRead,
    status_code=status.HTTP_201_CREATED,
)
def agregar_categoria(
    session: SessionDep, id: int = Path(..., gt=0), categoria_id: int = Path(..., gt=0)
):
    return service.vincular_categoria(session, id, categoria_id)


@router.delete("/{id}/categorias/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def quitar_categoria(
    session: SessionDep, id: int = Path(..., gt=0), categoria_id: int = Path(..., gt=0)
):
    service.desvincular_categoria(session, id, categoria_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
