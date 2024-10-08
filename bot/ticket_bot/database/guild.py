import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class Guild(Base):
    __tablename__ = "guild"

    id: Mapped[int] = mapped_column(sqlalchemy.BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(sqlalchemy.String(length=50))
