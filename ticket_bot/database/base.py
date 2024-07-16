from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    def __repr__(self) -> str:

        def parser(col: str):
            value = getattr(self, col, None)
            if not isinstance(value, (int, float)):
                value = f"{value}"
            return f"{col}={value}"

        return f"<{self.__class__.__name__}({', '.join([parser(col) for col in self.__table__.columns.keys()])})>"
