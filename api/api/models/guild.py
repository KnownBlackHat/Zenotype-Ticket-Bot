import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Guild(Base):
    __tablename__ = "guilds"

    guild: Mapped[int] = mapped_column(sqlalchemy.BigInteger, unique=True)
    name: Mapped[str] = mapped_column(sqlalchemy.String)

    icon: Mapped[str] = mapped_column(sqlalchemy.String, nullable=True)
    description: Mapped[str] = mapped_column(sqlalchemy.Text, nullable=True)
    owner: Mapped[int] = mapped_column(sqlalchemy.BigInteger, nullable=True)

    panels = relationship(
        "Panel", back_populates="guild", passive_deletes=True, lazy="selectin"
    )

    teams = relationship(
        "Team", back_populates="guild", passive_deletes=True, lazy="selectin"
    )

    messages = relationship(
        "Message", back_populates="guild", passive_deletes=True, lazy="selectin"
    )

    role = relationship(
        "Role",
        back_populates="guild",
        passive_deletes=True,
        lazy="selectin",
        uselist=False,
    )
