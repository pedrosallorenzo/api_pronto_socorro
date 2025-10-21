from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, Integer, String, Enum, ForeignKey, DateTime, func
from src.models.pessoa import Base


class TriagemModel(Base):
    __tablename__ = "tb_triagem"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )  # Chave primária da tabela tb_triagem
    id_paciente: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("tb_paciente.id_pessoa"), nullable=False
    )  # Chave estrangeira para tb_paciente

    pa: Mapped[str | None] = mapped_column(String(15), nullable=True)
    pulso: Mapped[int | None] = mapped_column(nullable=True)
    saturacao: Mapped[int | None] = mapped_column(nullable=True)
    temperatura: Mapped[float | None] = mapped_column(nullable=True)
    sintomas: Mapped[str | None] = mapped_column(nullable=True)

    prioridade: Mapped[str] = mapped_column(
        Enum("LEVE", "MODERADA", "ALTA"), nullable=False
    )
    id_especialidade_requisitada: Mapped[int] = mapped_column(Integer, nullable=False)
    id_leito: Mapped[int | None] = mapped_column(nullable=True)

    criado_em: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
