import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Guild(Base):
    __tablename__ = "guilds"

    guild: Mapped[int] = mapped_column(sqlalchemy.BigInteger, unique=True)
    name: Mapped[str] = mapped_column(sqlalchemy.String)

    icon: Mapped[str] = mapped_column(sqlalchemy.String)
    permissions: Mapped[int] = mapped_column(sqlalchemy.BigInteger)
    description: Mapped[str] = mapped_column(sqlalchemy.Text)
    owner: Mapped[int] = mapped_column(sqlalchemy.BigInteger)

    panels = relationship(
        "Panel", back_populates="guild", passive_deletes=True, lazy="selectin"
    )

    teams = relationship(
        "Team", back_populates="guild", passive_deletes=True, lazy="selectin"
    )

    messages = relationship(
        "Message", back_populates="guild", passive_deletes=True, lazy="selectin"
    )
