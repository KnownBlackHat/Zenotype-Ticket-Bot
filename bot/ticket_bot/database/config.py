import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from .guild import Guild


class Config(Base):
    __tablename__ = "config"

    guild_id: Mapped[int] = mapped_column(
        sqlalchemy.ForeignKey("guilds.id", ondelete="CASCADE"), index=True
    )

    title: Mapped[str] = mapped_column(sqlalchemy.String)
    description: Mapped[str] = mapped_column(sqlalchemy.String)
    img_url: Mapped[str] = mapped_column(sqlalchemy.String)

    guild: Mapped[Guild] = relationship(passive_deletes=True)
