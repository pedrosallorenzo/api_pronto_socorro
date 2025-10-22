from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Enum, ForeignKey, String
from src.models.pessoa import Base


class FuncionarioModel(Base):
    __tablename__ = "tb_funcionario"
    id_pessoa: Mapped[int] = mapped_column(
        Integer, ForeignKey("tb_pessoa.id"), primary_key=True
    )
    cargo: Mapped[str] = mapped_column(
        Enum("MEDICO", "ENFERMEIRO", "TEC_ENF"), nullable=False
    )
    conselho: Mapped[str | None] = mapped_column(String(50), nullable=True)
