# Cria os endpoints dos pacientes e rota com validação, transação e tratamento de erro

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)  # cria rotas e 'injeta' dependências
from sqlalchemy.orm import Session
from src.schemas.paciente import PacienteIn, PacienteOut  # contratos de entrada/saída
from src.repos.paciente_repo import PacienteRepo  # persiste no DB
from db.db import get_session  # fornece Session por request

router = APIRouter(prefix="/pacientes", tags=["Pacientes"])
# agrupa endpoints sob /pacientes e organiza no Swagger


@router.post("", response_model=PacienteOut)
def criar_paciente(payload: PacienteIn, db: Session = Depends(get_session)):
    # endpoint POST /pacientes com corpo validado por PacienteIn
    # injeta a Session do SQLAlchemy via Depends(get_session)
    repo = PacienteRepo(db)
    try:
        id_pessoa = repo.criar(**payload.model_dump())  # cria pessoa+paciente
        db.commit()  # confirma
        pessoa, paciente = repo.obter(id_pessoa)  # recarrega para responder
        return {
            "id_pessoa": pessoa.id,
            "nome": pessoa.nome,
            "tipo_sanguineo": paciente.tipo_sanguineo,
        }
    except Exception as e:
        db.rollback()  # reverte no erro
        raise HTTPException(status_code=400, detail=str(e))
