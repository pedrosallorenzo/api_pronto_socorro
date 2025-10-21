from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, Enum, DateTime, ForeignKey
from sqlalchemy.sql import func
from src.models.pessoa import Base


class AtendimentoModel(Base):
    __tablename__ = "tb_atendimento"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    id_paciente: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("tb_paciente.id_pessoa"), nullable=False
    )
    id_triagem: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("triagem.id"), nullable=False
    )
    id_profissional: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("funcionario.id_pessoa"), nullable=False
    )

    tipo: Mapped[str] = mapped_column(Enum("ENFERMAGEM", "MEDICO"), nullable=False)
    status: Mapped[str] = mapped_column(
        Enum("AGUARDANDO", "EM_ANDAMENTO", "FINALIZADO"),
        nullable=False,
        default="AGUARDANDO",
    )

    # >>> Anote com tipos Python (datetime | None) e use DateTime no mapped_column
    iniciado_em: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    finalizado_em: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    criado_em: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
