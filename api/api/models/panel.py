from datetime import UTC, datetime

import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Panel(Base):
    __tablename__ = "panels"

    title: Mapped[str] = mapped_column(sqlalchemy.String)
    description: Mapped[str] = mapped_column(sqlalchemy.Text)
    thumbnail: Mapped[str] = mapped_column(sqlalchemy.String)
    image: Mapped[str] = mapped_column(sqlalchemy.String)
    color: Mapped[str] = mapped_column(sqlalchemy.Text)
    createdAt: Mapped[int] = mapped_column(
        sqlalchemy.DateTime, default=datetime.now(UTC)
    )
    updatedAt: Mapped[int] = mapped_column(
        sqlalchemy.DateTime, onupdate=datetime.now(UTC)
    )

    category: Mapped[int] = mapped_column(sqlalchemy.BigInteger)

    guild_id: Mapped[int] = mapped_column(
        sqlalchemy.ForeignKey("guilds.id", ondelete="CASCADE"), index=True
    )
    guild = relationship("Guild", back_populates="panels")
