import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

# Lee el archivo .env (si existe). Una variable de entorno ya definida tiene prioridad.
load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:password@localhost:5432/tp_productos",
)

# Una única instancia global del engine para toda la aplicación.
engine = create_engine(DATABASE_URL, echo=False)


def create_db_and_tables() -> None:
    # Crea las tablas de los modelos con table=True que ya fueron importados.
    SQLModel.metadata.create_all(engine)


def get_session():
    # Una sesión (transacción) por request; se cierra sola al terminar.
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


def guardar(session: Session, obj: SQLModel) -> SQLModel:
    # add() registra, commit() ejecuta la transacción y refresh() recarga el objeto (id generado).
    try:
        session.add(obj)
        session.commit()
    except Exception:
        session.rollback()
        raise
    session.refresh(obj)
    return obj
