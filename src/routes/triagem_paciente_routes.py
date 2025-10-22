# Facilitar o fluxo criando um endpoint para fazer os dois cadastros


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.db import get_session
from src.schemas.triagem_paciente import CadastrarPacienteETriagemIn, PacienteTriagemOut
from src.services.triagem_ext_service import PacienteTriagemService

router = APIRouter(prefix="/cadastro", tags=["Cadastro rápido"])


@router.post("/paciente-triagem", response_model=PacienteTriagemOut)
def cadastrar(payload: CadastrarPacienteETriagemIn, db: Session = Depends(get_session)):
    try:
        id_pessoa, id_triagem = PacienteTriagemService(db).cadastrar_paciente_e_triagem(
            payload.model_dump()
        )
        return {"id_pessoa": id_pessoa, "id_triagem": id_triagem}
    except Exception as e:
        db.rollback()
        raise HTTPException(400, str(e))
