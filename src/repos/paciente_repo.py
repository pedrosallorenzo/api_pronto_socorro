from sqlalchemy.orm import Session
from src.models.pessoa import PessoaModel
from src.models.paciente import PacienteModel
from datetime import date


class PacienteRepo:
    def __init__(self, db: Session):
        self.db = db  # Transação a cada request

    def criar(
        self,
        *,
        nome: str,
        cpf: str,
        dt_nascimento: str,
        telefone: str | None,
        tipo_sanguineo: str,
        historico_medico: str | None
    ) -> int:

        pessoa = PessoaModel(  # Cria o 'objeto' Pessoa
            nome=nome,
            cpf=cpf,
            telefone=telefone,
            dt_nascimento=date.fromisoformat(dt_nascimento),
            # converte str para date
        )
        self.db.add(pessoa)
        self.db.flush()
        # O flush registra no BD e preenche pessoa.id sem commitar

        # cria Paciente vinculado
        paciente = PacienteModel(
            id_pessoa=pessoa.id,
            tipo_sanguineo=tipo_sanguineo,
            historico_medico=historico_medico,
        )
        self.db.add(paciente)
        self.db.flush()

        return pessoa.id
        # retorna o id gerado sendo a própria chave primária

    def obter(self, id_pessoa: int) -> tuple[PessoaModel, PacienteModel] | None:
        pes = self.db.get(PessoaModel, id_pessoa)
        if not pes:
            return None
        pac = self.db.get(PacienteModel, id_pessoa)
        if not pac:
            return None
        return pes, pac
