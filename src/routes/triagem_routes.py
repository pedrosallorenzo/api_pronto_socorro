from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schemas.triagem import TriagemIn, TriagemOut  # contratos
from src.services.triagem_service import TriagemService  # regras
from db.db import get_session  # sessão por request

router = APIRouter(prefix="/triagens", tags=["Triagens"])


@router.post("", response_model=TriagemOut)
def abrir_triagem(payload: TriagemIn, db: Session = Depends(get_session)):
    # POST /triagens
    svc = TriagemService(db)  # instancia o serviço
    try:
        triagem_id = svc.abrir_triagem(payload.model_dump())
        # chama a regra (valida paciente e grava)
        return {
            "id": triagem_id,
            "id_paciente": payload.id_paciente,
            "prioridade": payload.prioridade,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
