from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import create_db_and_tables
# Importar los modelos registra las tablas en SQLModel.metadata antes de create_all().
from app.categoria import model as categoria_model  # noqa: F401
from app.producto import model as producto_model  # noqa: F401
from app.categoria.router import router as categoria_router
from app.producto.router import router as producto_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="API Productos y Categorías - Unidad 6",
    description="CRUD de Categorías (consumido por React) y de Productos con su relación N:M.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS: permite que el frontend (Vite, puerto 5173) llame a esta API (puerto 8000).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(categoria_router)
app.include_router(producto_router)
