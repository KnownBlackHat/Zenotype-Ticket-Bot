import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Ticket(Base):
    __tablename__ = "tickets"

    userId: Mapped[int] = mapped_column(sqlalchemy.BigInteger)

    # Relationship
    panel_id: Mapped[int] = mapped_column(
        sqlalchemy.ForeignKey("panels.id", ondelete="CASCADE"), index=True
    )
    panel = relationship("Panel", back_populates="tickets")
    messages = relationship("Message", back_populates="ticket", lazy="selectin")
