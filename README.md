# TP6 – CRUD Categorías + CRUD Productos (Programación IV, Unidad 6)

Aplicación Full Stack: frontend **React + TypeScript + Tailwind** que consume una API **FastAPI + SQLModel + PostgreSQL**.

```
backend/    API FastAPI (app/core, app/categoria, app/producto) + tests/*.http
frontend/   React + TS + Vite + Tailwind (CRUD de Categorías)
```

## 1. Backend

Requisitos: Python 3.10–3.13 y PostgreSQL en ejecución.

1. Crear la base vacía `tp_productos` (pgAdmin: *Databases → Create → Database*).
2. Editar `backend/.env` y poner la contraseña real:
   ```
   DATABASE_URL=postgresql+psycopg://postgres:TU_PASSWORD@localhost:5432/tp_productos
   ```
3. Instalar y ejecutar (desde `backend/`):
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   python -m fastapi dev app/main.py
   ```
   Las tablas `categoria`, `producto` y `productocategoria` se crean solas al iniciar.
   Documentación interactiva: http://127.0.0.1:8000/docs

### Endpoints

| Recurso | Endpoints |
|---------|-----------|
| Categorías | `GET /categorias`, `GET /categorias/{id}`, `POST /categorias`, `PUT /categorias/{id}`, `DELETE /categorias/{id}` |
| Productos | `GET /productos`, `GET /productos/{id}`, `POST /productos`, `PUT /productos/{id}`, `DELETE /productos/{id}` |
| Producto ↔ Categoría | `GET /productos/{id}/categorias`, `POST /productos/{id}/categorias/{categoria_id}`, `DELETE /productos/{id}/categorias/{categoria_id}` |

Reglas: nombre único (sin distinguir mayúsculas) → `409`; id inexistente → `404`; datos inválidos → `422`.
Al eliminar una categoría o un producto se borran también sus vínculos en la tabla intermedia.

### Demostración con REST Client

Archivos en `backend/tests/`: `productos.http` (CRUD de productos + relación) y `categorias.http`.
Abrirlos en VS Code con la extensión *REST Client* y ejecutar las peticiones en orden.

### Notas de diseño

- `precio_base` es numérico (`float`, `>= 0`) aunque el enunciado lo muestra como `str`: un precio debe poder validarse y ordenarse.
- `imagen_url` es una lista de strings guardada en una columna JSON.
- `ProductoCategoria` tiene clave primaria compuesta (`producto_id`, `categoria_id`), así no hay vínculos repetidos.
- CORS permite el origen `http://localhost:5173`.

## 2. Frontend

Requisitos: Node y pnpm. Con el backend ya corriendo (desde `frontend/`):

```bash
pnpm install
pnpm build   # verifica tipos con tsc -b
pnpm dev     # http://localhost:5173
```

- `App.tsx` concentra `useState`/`useEffect` y las funciones `handleCreate`, `handleUpdate`, `handleDelete` (fetch nativo).
- `CategoriaModal` es el formulario de alta/edición y usa el hook `useForm` (`src/hooks`).
- Tipos en `src/types/` (`Categoria`, `Producto`); componentes con props tipados en `src/components/`.
