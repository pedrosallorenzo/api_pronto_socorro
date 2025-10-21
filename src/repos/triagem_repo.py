# Grava as triagens

from sqlalchemy.orm import Session
from src.models.triagem import TriagemModel


class TriagemRepo:
    def __init__(self, db: Session):
        self.db = db

    def criar(self, **dados) -> int:
        t = TriagemModel(**dados)  # cria o objeto ORM com os dados de entrada
        self.db.add(t)
        self.db.flush()  # insere e materializa o id
        return t.id  # retorna o id gerado
