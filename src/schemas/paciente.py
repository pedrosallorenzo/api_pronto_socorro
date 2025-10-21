from pydantic import BaseModel, Field


class PacienteIn(BaseModel):
    nome: str
    cpf: str = Field(
        min_length=11, max_length=11
    )  # Delimita o tamanho padrão de um CPF
    dt_nascimento: str  # Ano, mês e dia # Traduzida para date no repo
    telefone: str | None = None
    tipo_sanguineo: str
    historico_medico: str | None = None


class PacienteOut(BaseModel):
    id_pessoa: int
    nome: str
    tipo_sanguineo: str
