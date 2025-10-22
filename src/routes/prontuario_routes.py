# Apenas mostra o estado clínico mais recente do paciente


from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.db import get_session
from src.services.prontuario_service import ProntuarioService
from src.security import require_role

router = APIRouter(prefix="/prontuario", tags=["Prontuario"])


@router.get(
    "/{id_pessoa}",
    dependencies=[Depends(require_role("MEDICO", "ENFERMEIRO", "TEC_ENF"))],
)
def prontuario(id_pessoa: int, db: Session = Depends(get_session)):
    return ProntuarioService(db).resumo_por_paciente(id_pessoa)
