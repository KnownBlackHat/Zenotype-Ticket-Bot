import sqlalchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):

    id: Mapped[int] = mapped_column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True, index=True
    )

    def __repr__(self) -> str:

        def parser(col: str):
            value = getattr(self, col, None)
            if not isinstance(value, (int, float)):
                value = f"{value}"
            return f"{col}={value}"

        return f"<{self.__class__.__name__}({', '.join([parser(col) for col in self.__table__.columns.keys()])})>"
