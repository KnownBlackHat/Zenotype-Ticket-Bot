from datetime import datetime

import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Tickets(Base):
    __tablename__ = "ticketlist"

    id: Mapped[int] = mapped_column(sqlalchemy.Integer, primary_key=True)

    openedBy: Mapped[int] = mapped_column(sqlalchemy.Integer)
    closedBy: Mapped[int] = mapped_column(sqlalchemy.Integer, nullable=True)
    claimedBy: Mapped[int] = mapped_column(sqlalchemy.Integer, nullable=True)
    opentime: Mapped[datetime] = mapped_column(sqlalchemy.DateTime)
    reason: Mapped[str] = mapped_column(sqlalchemy.String, nullable=True)
    configid: Mapped[int] = mapped_column(sqlalchemy.Integer)
