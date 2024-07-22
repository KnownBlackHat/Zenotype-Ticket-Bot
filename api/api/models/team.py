import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Team(Base):
    __tablename__ = "teams"

    user: Mapped[int] = mapped_column(sqlalchemy.BigInteger)
    team: Mapped[str] = mapped_column(sqlalchemy.Text)

    guild_id: Mapped[int] = mapped_column(
        sqlalchemy.ForeignKey("guilds.id", ondelete="CASCADE"), index=True
    )
    guild = relationship("Guild", back_populates="teams")
