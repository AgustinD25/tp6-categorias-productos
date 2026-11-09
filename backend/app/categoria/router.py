from typing import List

from fastapi import APIRouter, HTTPException, Path, Response, status

from app.core.database import SessionDep
from . import schema, service

router = APIRouter(prefix="/categorias", tags=["Categorías"])

NO_ENCONTRADA = "Categoría no encontrada"


@router.get("", response_model=List[schema.CategoriaRead])
def listar_categorias(session: SessionDep):
    return service.obtener_todas(session)


@router.get("/{id}", response_model=schema.CategoriaRead)
def detalle_categoria(session: SessionDep, id: int = Path(..., gt=0)):
    categoria = service.obtener_por_id(session, id)
    if not categoria:
        raise HTTPException(status.HTTP_404_NOT_FOUND, NO_ENCONTRADA)
    return categoria


@router.post("", response_model=schema.CategoriaRead, status_code=status.HTTP_201_CREATED)
def crear_categoria(categoria: schema.CategoriaCreate, session: SessionDep):
    return service.crear(session, categoria)


@router.put("/{id}", response_model=schema.CategoriaRead)
def actualizar_categoria(
    categoria: schema.CategoriaCreate, session: SessionDep, id: int = Path(..., gt=0)
):
    actualizada = service.actualizar(session, id, categoria)
    if not actualizada:
        raise HTTPException(status.HTTP_404_NOT_FOUND, NO_ENCONTRADA)
    return actualizada


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_categoria(session: SessionDep, id: int = Path(..., gt=0)):
    if not service.eliminar(session, id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, NO_ENCONTRADA)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
