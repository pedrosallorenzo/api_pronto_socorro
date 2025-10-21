from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, Enum, ForeignKey
from .pessoa import Base


class PacienteModel(Base):
    __tablename__ = "tb_paciente"

    id_pessoa: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("tb_pessoa.id"), primary_key=True
    )
    tipo_sanguineo: Mapped[str] = mapped_column(
        Enum("A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"), nullable=False
    )
    historico_medico: Mapped[str | None]
