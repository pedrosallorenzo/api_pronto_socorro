# Aplica RBAC nas filas e entrega os dados prontos pro frontend (interfaces)


from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.db import get_session
from src.services.filas_service import FilasService
from src.security import require_role

router = APIRouter(prefix="/filas", tags=["Filas"])


@router.get("/medico", dependencies=[Depends(require_role("MEDICO"))])
def fila_medico(db: Session = Depends(get_session)):
    return FilasService(db).fila_medico()


@router.get(
    "/enfermagem", dependencies=[Depends(require_role("ENFERMEIRO", "TEC_ENF"))]
)
def fila_enfermagem(db: Session = Depends(get_session)):
    return FilasService(db).fila_enfermagem()
