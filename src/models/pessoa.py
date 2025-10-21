from datetime import date
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import BigInteger, String, Date

Base = declarative_base()


class PessoaModel(Base):
    __tablename__ = "tb_pessoa"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(200), nullable=False)
    cpf: Mapped[str] = mapped_column(String(11), nullable=False, unique=True)
    telefone: Mapped[str | None] = mapped_column(String(20), nullable=True)

    dt_nascimento: Mapped[date] = mapped_column(Date, nullable=False)
