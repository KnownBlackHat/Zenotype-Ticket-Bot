from datetime import UTC, datetime

import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Message(Base):
    __tablename__ = "messages"

    userId: Mapped[int] = mapped_column(sqlalchemy.BigInteger)
    userName: Mapped[str] = mapped_column(sqlalchemy.String)
    channel: Mapped[int] = mapped_column(sqlalchemy.BigInteger)
    message: Mapped[str] = mapped_column(sqlalchemy.Text)
    panel: Mapped[str] = mapped_column(sqlalchemy.String)

    createdAt: Mapped[int] = mapped_column(
        sqlalchemy.DateTime, default=datetime.now(UTC)
    )
    updatedAt: Mapped[int] = mapped_column(
        sqlalchemy.DateTime, onupdate=datetime.now(UTC), nullable=True
    )

    # Relationship
    ticket_id: Mapped[int] = mapped_column(
        sqlalchemy.ForeignKey("tickets.id", ondelete="CASCADE"), index=True
    )
    ticket = relationship("Ticket", back_populates="messages")
