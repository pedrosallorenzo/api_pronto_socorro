from pydantic import BaseModel

class TriagemIn(BaseModel):
    id_paciente: int
    pa: str | None = None
    pulso: int | None = None
    saturacao: int | None = None
    temperatura: float | None = None
    sintomas: str | None = None
    prioridade: str
    id_especialidade_requisitada: int
    id_leito: int | None = None

class TriagemOut(BaseModel):
    id: int
    id_paciente: int
    prioridade: str