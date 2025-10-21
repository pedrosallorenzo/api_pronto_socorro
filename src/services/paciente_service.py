from sqlalchemy.orm import Session
from sqlalchemy import select
from models.pessoa import PessoaModel
from src.repos.paciente_repo import PacienteRepo


class PacientesService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = PacienteRepo(db)

    @staticmethod
    def _somente_digitos(cpf: str) -> str:
        return "".join(ch for ch in cpf if ch.isdigit())

    def _validar_cpf_bruto(self, cpf: str) -> str:
        cpf_digits = self._somente_digitos(cpf)
        if len(cpf_digits) != 11:
            raise ValueError("CPF deve conter 11 dígitos (somente números).")
        return cpf_digits

    def _assegurar_cpf_unico(
        self, cpf_digits: str
    ) -> None:  # Verifica a unicidade do CPF
        existe = self.db.execute(
            select(PessoaModel.id).where(PessoaModel.cpf == cpf_digits)
        ).scalar_one_or_none()
        if existe:
            raise ValueError("Já existe paciente (pessoa) com este CPF.")

    def criar_paciente(  # Cria Pessoa e Paciente depois
        # da verificação do CPF
        self,
        *,
        nome: str,
        cpf: str,
        dt_nascimento: str,
        telefone: str | None,
        tipo_sanguineo: str,
        historico_medico: str | None
    ) -> int:
        cpf_digits = self._validar_cpf_bruto(cpf)
        self._assegurar_cpf_unico(cpf_digits)

        id_pessoa = self.repo.criar(  # Chama o repositório que insere nas duas tabelas e retorna o id_pessoa
            nome=nome,
            cpf=cpf_digits,
            dt_nascimento=dt_nascimento,
            telefone=telefone,
            tipo_sanguineo=tipo_sanguineo,
            historico_medico=historico_medico,
        )
        self.db.commit()
        return id_pessoa

    def obter_paciente(
        self, id_pessoa: int
    ) -> dict:  # Retorna um dict para Pessoa + Paciente juntos
        res = self.repo.obter(id_pessoa)
        if not res:
            raise ValueError("Paciente não encontrado.")
        pessoa, paciente = res
        return {
            "id_pessoa": pessoa.id,
            "nome": pessoa.nome,
            "cpf": pessoa.cpf,
            "telefone": pessoa.telefone,
            "dt_nascimento": pessoa.dt_nascimento.isoformat(),
            "tipo_sanguineo": paciente.tipo_sanguineo,
            "historico_medico": paciente.historico_medico,
        }

    def listar_pacientes(
        self, offset: int = 0, limit: int = 50
    ) -> list[dict]:  # Lista pessoas/pacientes de forma paginada (join).
        stmt = (
            select(
                PessoaModel.id,
                PessoaModel.nome,
                PessoaModel.cpf,
                PessoaModel.telefone,
                PessoaModel.dt_nascimento,
            )
            .offset(offset)
            .limit(limit)
            .order_by(PessoaModel.id.desc())
        )
        pessoas = self.db.execute(stmt).all()

        return [
            {
                "id_pessoa": row.id,
                "nome": row.nome,
                "cpf": row.cpf,
                "telefone": row.telefone,
                "dt_nascimento": row.dt_nascimento.isoformat(),
            }
            for row in pessoas
        ]
