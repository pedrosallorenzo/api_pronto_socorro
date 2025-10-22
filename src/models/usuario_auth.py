from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, DateTime, String, ForeignKey
from src.models.pessoa import Base


class UsuarioAuthModel(Base):
    __tablename__ = "tb_usuario_auth"
    id_funcionario: Mapped[int] = mapped_column(
        Integer, ForeignKey("tb_funcionario.id_pessoa"), primary_key=True
    )
    hash_senha: Mapped[str] = mapped_column(String(255), nullable=False)
    ultimo_login: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    bloqueado: Mapped[int] = mapped_column(default=0)
