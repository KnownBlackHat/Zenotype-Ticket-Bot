from datetime import UTC, datetime

import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Panel(Base):
    __tablename__ = "panels"

    # Panel Message
    title: Mapped[str] = mapped_column(sqlalchemy.String)
    description: Mapped[str] = mapped_column(sqlalchemy.Text)
    color: Mapped[str] = mapped_column(sqlalchemy.Text)
    disable_panel: Mapped[bool] = mapped_column(sqlalchemy.Boolean, default=False)

    # Panel Button
    button_color: Mapped[str] = mapped_column(sqlalchemy.Text)
    button_text: Mapped[str] = mapped_column(sqlalchemy.Text)
    button_emoji: Mapped[str] = mapped_column(sqlalchemy.Text)

    # Ticket Properties
    mention_on_open: Mapped[int] = mapped_column(sqlalchemy.BigInteger)
    support_team: Mapped[str] = mapped_column(
        sqlalchemy.Text
    )  # TODO: This should be linked to team table
    category: Mapped[int] = mapped_column(sqlalchemy.BigInteger)
    naming_scheme = mapped_column(sqlalchemy.String)

    # Images
    large_image: Mapped[str] = mapped_column(sqlalchemy.String, nullable=True)
    small_image: Mapped[str] = mapped_column(sqlalchemy.String, nullable=True)

    # Welcome Message
    wlcm_title: Mapped[str] = mapped_column(sqlalchemy.String, nullable=True)
    wlcm_description: Mapped[str] = mapped_column(sqlalchemy.String, nullable=True)
    wlcm_color: Mapped[str] = mapped_column(sqlalchemy.String, nullable=True)

    # Author
    author_name: Mapped[str] = mapped_column(sqlalchemy.String)
    author_url: Mapped[str] = mapped_column(sqlalchemy.String, nullable=True)

    # Access Control
    roles: Mapped[int] = mapped_column(sqlalchemy.BigInteger)

    # Metadata
    createdAt: Mapped[int] = mapped_column(
        sqlalchemy.DateTime, default=datetime.now(UTC)
    )
    updatedAt: Mapped[int] = mapped_column(
        sqlalchemy.DateTime, onupdate=datetime.now(UTC), nullable=True
    )

    # Relationship
    category: Mapped[int] = mapped_column(sqlalchemy.BigInteger)

    guild_id: Mapped[int] = mapped_column(
        sqlalchemy.ForeignKey("guilds.id", ondelete="CASCADE"), index=True
    )
    guild = relationship("Guild", back_populates="panels")

    tickets = relationship("Ticket", back_populates="panel", lazy="selectin")
