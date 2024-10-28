import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .guild import Guild


class TicketConfig(Base):
    __tablename__ = "config"

    id: Mapped[int] = mapped_column(sqlalchemy.Integer, primary_key=True, index=True)
    guild_id: Mapped[int] = mapped_column(
        sqlalchemy.ForeignKey("guild.id", ondelete="CASCADE"), index=True
    )

    title: Mapped[str] = mapped_column(sqlalchemy.String)
    description: Mapped[str] = mapped_column(sqlalchemy.String)
    img_url: Mapped[str] = mapped_column(sqlalchemy.String)
    # role: Mapped[int] = mapped_column(sqlalchemy.BigInteger)

    config: Mapped[int] = mapped_column(sqlalchemy.BigInteger, index=True)
    # category: Mapped[int] = mapped_column(sqlalchemy.BigInteger)
    transcript: Mapped[int] = mapped_column(sqlalchemy.BigInteger)

    color: Mapped[int] = mapped_column(sqlalchemy.Integer)

    # Relations
    guild: Mapped[Guild] = relationship(passive_deletes=True)
