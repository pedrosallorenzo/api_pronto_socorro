# Cria a regra de que se não tiver registro do paciente, não haverá triagem

from sqlalchemy.orm import Session
from src.repos.paciente_repo import PacienteRepo
from src.repos.triagem_repo import TriagemRepo


class TriagemService:
    def __init__(self, db: Session):
        self.db = db
        self.pacientes = PacienteRepo(db)  # repositório de pacientes
        self.triagens = TriagemRepo(db)  # repositório de triagens

    def abrir_triagem(self, dados: dict) -> int:
        existe = self.pacientes.obter(dados["id_paciente"])
        if not existe:
            raise ValueError("Paciente não encontrado.")

        triagem_id = self.triagens.criar(**dados)
        self.db.commit()  # confirma a transação
        return triagem_id
